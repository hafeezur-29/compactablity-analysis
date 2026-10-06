async function analyze(){
  const url=document.getElementById("url").value.trim();
  if(!url)return alert("Enter a website URL");
  const btn=document.querySelector("button"); btn.disabled=true; btn.textContent="Analyzing...";
  try{
    const r=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url})});
    const d=await r.json(); if(!r.ok)throw Error(d.error);
    const s=d.scan,q=d.requirements;
    document.getElementById("summary").innerHTML=`
      <div class="card"><small>STATUS</small><b>${s.status}</b></div>
      <div class="card"><small>RESPONSE</small><b>${s.load_ms} ms</b></div>
      <div class="card"><small>EST. RAM</small><b>${q.ram} GB</b></div>
      <div class="card"><small>RECOMMENDED</small><b>${d.recommended}</b></div>`;
    document.getElementById("machines").innerHTML=d.machines.map(m=>`
      <div class="machine ${m.ok?"ok":""}">
        <h3>${m.name}</h3><p>CPU: ${m.cpu} vCPU</p><p>RAM: ${m.ram} GB</p><p>Storage: ${m.storage} GB</p>
        <span class="badge">${m.ok?"Compatible":"Insufficient"}</span>
      </div>`).join("");
    document.getElementById("result").classList.remove("hidden");
    document.getElementById("result").scrollIntoView({behavior:"smooth"});
  }catch(e){alert(e.message)}
  finally{btn.disabled=false;btn.textContent="Analyze"}
}
