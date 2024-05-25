const axios = require('axios');

const index = async function (req, res){
    res.render('index', { text: 'This is EJS'})
}

const about = async function (req, res){
    res.render('about', { text: 'About Page'})
}


module.exports = { index, about }