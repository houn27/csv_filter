const {createProxyMiddleware}=require('http-proxy-middleware');

//export anonymous function as defult module name: setupProxy
module.exports=function(app){
    //console.log("setupProxy.js is running !!")
    app.use(
    createProxyMiddleware('/filter',{
        target:'http://localhost:8000',
        changeOrigin:true,
        pathRewrite: {'^/filter': ''}
        })   
    )

}