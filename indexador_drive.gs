/**
 * CAUC v22 — índice privado dos CSVs no Google Drive.
 * Instalação pelo proprietário da pasta, uma única vez:
 * 1. Acesse https://script.google.com/ e crie um Novo projeto.
 * 2. Substitua o conteúdo de Código.gs por este arquivo inteiro.
 * 3. Salve, escolha prepararIndice no seletor de funções e clique Executar.
 * 4. Autorize com a conta que pode editar a pasta BD CAUC.
 * 5. A função cria indice_cauc.json na própria pasta e um acionador de 5 minutos.
 * Não publique como aplicativo Web. Não coloque este JSON no GitHub.
 * Os usuários do dashboard continuam Leitores da pasta, sem poder de escrita.
 * Para forçar atualização após enviar um CSV: execute atualizarIndice.
 * Para desligar a automação: execute removerAcionadorIndice.
 */
const CAUC_FOLDER_ID='1pKwXBmXA9hssDVHoTKoQLnOt5n1uXuku';
const CAUC_INDEX_NAME='indice_cauc.json';
function prepararIndice(){
  atualizarIndice();
  const triggers=ScriptApp.getProjectTriggers().filter(t=>t.getHandlerFunction()==='atualizarIndice');
  if(!triggers.length)ScriptApp.newTrigger('atualizarIndice').timeBased().everyMinutes(5).create();
  Logger.log('Pronto. Índice privado criado em BD CAUC; atualização a cada 5 minutos (sujeita às cotas do Apps Script).');
}
function removerAcionadorIndice(){
  ScriptApp.getProjectTriggers().filter(t=>t.getHandlerFunction()==='atualizarIndice').forEach(t=>ScriptApp.deleteTrigger(t));
  Logger.log('Acionadores deste projeto removidos. O arquivo do índice foi mantido.');
}
function caucDataValida_(y,m,d){
  const iso=[String(y).padStart(4,'0'),String(m).padStart(2,'0'),String(d).padStart(2,'0')].join('-');
  const date=new Date(iso+'T00:00:00Z');
  return Number.isFinite(+date)&&date.toISOString().slice(0,10)===iso?iso:null;
}
function caucData_(text){
  let m=String(text||'').match(/\b(\d{4})[-_.\/](\d{2})[-_.\/](\d{2})\b/);
  if(m)return caucDataValida_(+m[1],+m[2],+m[3]);
  m=String(text||'').match(/\b(\d{2})[-_.\/](\d{2})[-_.\/](\d{4})\b/);
  return m?caucDataValida_(+m[3],+m[2],+m[1]):null;
}
function caucLerData_(file){
  const blob=file.getBlob();
  let text=blob.getDataAsString('UTF-8');
  if(text.indexOf('\uFFFD')>=0)text=blob.getDataAsString('Windows-1252');
  const lines=text.replace(/^\uFEFF/,'').split(/\r?\n/);
  const dataLine=lines.slice(0,40).find(l=>/data\s+(da\s+pesquisa|do\s+relat[oó]rio|de\s+pesquisa)/i.test(l));
  const date=caucData_(dataLine)||caucData_(file.getName());
  if(!date)throw new Error('Sem Data da Pesquisa e sem data válida no nome');
  if(!lines.some(l=>/cnpj/i.test(l)&&/1[.]\d/.test(l)))throw new Error('Cabeçalho de relatório CAUC não encontrado');
  return date;
}
function atualizarIndice(){
  const lock=LockService.getScriptLock();
  if(!lock.tryLock(10000))return;
  try{
    const root=DriveApp.getFolderById(CAUC_FOLDER_ID);
    const existing=root.getFilesByName(CAUC_INDEX_NAME);
    const indexFiles=[];
    while(existing.hasNext())indexFiles.push(existing.next());
    if(indexFiles.length>1)throw new Error('Há mais de um '+CAUC_INDEX_NAME+'. Mantenha somente um arquivo na pasta.');
    const indexFile=indexFiles[0]||null;
    let previous={};
    if(indexFile){
      try{
        const old=JSON.parse(indexFile.getBlob().getDataAsString('UTF-8'));
        if(old.schema_version===1&&old.folder_id===CAUC_FOLDER_ID)
          (old.files||[]).forEach(f=>{previous[f.id]=f;});
      }catch(e){Logger.log('Índice anterior ilegível; reconstruindo do zero.');}
    }
    const queue=[{folder:root,path:'BD CAUC'}],seen={},entries=[],errors=[];
    let revisados=0;
    while(queue.length){
      const node=queue.shift();const fid=node.folder.getId();
      if(seen[fid])continue;seen[fid]=true;
      const files=node.folder.getFiles();
      while(files.hasNext()){
        const file=files.next();const name=file.getName(),mime=file.getMimeType();
        if(file.getId()===(indexFile&&indexFile.getId()))continue;
        const isCsv=/\.csv$/i.test(name)||(['text/csv','application/csv','application/vnd.ms-excel'].indexOf(mime)>=0&&!/\.xlsx?$/i.test(name));
        if(!isCsv)continue;
        const id=file.getId();
        const meta={id,name,path:node.path+'/'+name,mimeType:mime,modifiedTime:file.getLastUpdated().toISOString(),size:String(file.getSize())};
        try{
          const old=previous[id];
          meta.report_date=old&&old.modifiedTime===meta.modifiedTime&&String(old.size)===meta.size&&old.report_date?
            old.report_date:caucLerData_(file);
          entries.push(meta);revisados++;
        }catch(e){errors.push(meta.path+': '+e.message);}
      }
      const folders=node.folder.getFolders();
      while(folders.hasNext()){
        const folder=folders.next();queue.push({folder,path:node.path+'/'+folder.getName()});
      }
    }
    entries.sort((a,b)=>a.report_date.localeCompare(b.report_date)||a.modifiedTime.localeCompare(b.modifiedTime));
    const latest=entries.length?entries[entries.length-1]:null;
    const payload={schema_version:1,folder_id:CAUC_FOLDER_ID,generated_at:new Date().toISOString(),
      latest_file_id:latest?latest.id:null,latest_report_date:latest?latest.report_date:null,files:entries,errors};
    const json=JSON.stringify(payload);
    // Atualiza no mesmo ID. Não abre compartilhamento público, não altera permissões.
    if(indexFile)indexFile.setContent(json);
    else root.createFile(CAUC_INDEX_NAME,json,'application/json');
    Logger.log('Índice atualizado: '+revisados+' CSVs; '+errors.length+' erro(s); última posição '+(latest?latest.report_date:'sem dados'));
    if(errors.length)Logger.log(errors.join('\n'));
  }finally{lock.releaseLock();}
}
