const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
    proxy: {
      '^/auth': {
        //запускать бэк на 8000 порту или поменять тут
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '^/back/classification-image': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      //todo тут захардкодил 6281
      '^/cnn_table/6281/add': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})

