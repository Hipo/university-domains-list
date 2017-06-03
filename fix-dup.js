const fs = require('fs');

let wuad = JSON.parse(fs.readFileSync('./world_universities_and_domains.json'));

let domains = [];
for(i in wuad){
  if(domains.indexOf(wuad[i].domain) !== -1){
    console.log(`${wuad[i].domain} - ${wuad[i].name} is duplicate`);
    continue;
  }
  domains.push(wuad[i].domain);
}
