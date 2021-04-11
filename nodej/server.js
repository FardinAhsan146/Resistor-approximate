const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;
app.use(express.static("public"));

app.get('/api', (req,res) =>{
    res.send('you DO not have permission to view page Proletariat!')
})

app.post("/api", (req, res) => {
    console.log(JSON.stringify(req));
    res.json('USERINPUT SUCCESSFUL')
});

app.listen(PORT, () => {
  console.log(`listening on http://localhost:${PORT}`);
  console.log(`listening on http://localhost:${PORT}/index.html`);
});
