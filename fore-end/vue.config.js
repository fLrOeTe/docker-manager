module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
    productionSourceMap: false,
    devServer: {
        overlay: {
            warnings: false,
            errors: false
        },
        port: 8000,
        proxy: {
            '':{
                target:'http://192.168.0.105:8000',
                changeOrigin:true,
                ws:false,
            },        
        }
    }
}