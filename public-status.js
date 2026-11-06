"use strict";
// Public GitHub Actions snapshot: no authentication, analytics, storage or private data.
(async function () {
  const grid=document.getElementById("ci-grid");
  const meta=document.getElementById("ci-asof");
  if (!grid || !meta) return;
  function show(message){
    grid.replaceChildren();
    const p=document.createElement("p");
    p.style.padding="1.5rem";
    p.textContent=message;
    grid.appendChild(p);
  }
  try {
    const response=await fetch("./public-status.json",{cache:"no-cache",credentials:"omit"});
    if(!response.ok)throw Error("Status snapshot unavailable");
    const payload=await response.json();
    if(!Array.isArray(payload.projects) || payload.projects.length!==8)throw Error("Invalid snapshot");
    grid.replaceChildren();
    for (const item of payload.projects){
      const card=document.createElement("a");
      card.className="ci-card";
      const allowed=typeof item.run_url==="string" && /^https:\/\/github\.com\/vishwasaithalz\/[\w-]+\/actions\/runs\/\d+$/.test(item.run_url);
      card.href=allowed?item.run_url:"https://github.com/vishwasaithalz/"+encodeURIComponent(item.repository||"");
      card.rel="noopener noreferrer";
      card.target="_blank";
      const title=document.createElement("strong");
      title.textContent=item.name||"Unverified project";
      const small=document.createElement("small");
      small.textContent=item.workflow||"No workflow";
      const badge=document.createElement("span");
      const states={passed:"✓ CI PASSED",failed:"! CHECK FAILED",running:"● CHECK RUNNING",unavailable:"? DATA UNAVAILABLE",not_verified:"? NOT VERIFIED"};
      const state=Object.hasOwn(states,item.state)?item.state:"not_verified";
      badge.className="ci-badge "+state;
      badge.textContent=states[state];
      card.append(title,small,badge);
      grid.appendChild(card);
    }
    if(payload.generated_at_utc){
      const timestamp=new Date(payload.generated_at_utc);
      meta.textContent=Number.isNaN(timestamp.valueOf())?"Snapshot timestamp unavailable":"Captured "+timestamp.toLocaleString()+" (your local time)";
    }else meta.textContent="First public CI snapshot pending";
  }catch(error){show("GitHub CI evidence is temporarily unavailable. Use the linked source and Actions pages for the latest verified records.");meta.textContent="Public status could not be fetched";}
})();
