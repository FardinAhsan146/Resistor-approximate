const express = require('express')

const app = express()
const PORT = process.env.PORT || 3000
app.use(express.static('public'))
app.get('/', (req, res) => {
    res.send('amogus ting tong!')
})
app.get('/api',(req,res)=>{
    res.json(
        {'qasam wallahi':'billah'}
    )
})
app.post('/', (req,res)=>{
    console.log(req.body)
})
app.listen(PORT, () =>{
    console.log(`listening on http://localhost:${PORT}`);
    console.log(`listening on http://localhost:${PORT}/index.html`);
})