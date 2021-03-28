console.log("frontend has loaded!");
const inputbox = document.getElementById("inputbox");
const submit = document.getElementById("submitbtn");

submit.addEventListener("click", async() => {
  const resp = await fetch(`http://localhost:3000/api`);
  if(resp.ok){
     resp.json().then(data => console.log(data)) 
  }else{
      console.error('error')
  }
  
});
