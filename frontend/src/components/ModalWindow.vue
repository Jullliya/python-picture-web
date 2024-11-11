<template>
  <div v-loading="loading">
    <el-upload
        class="upload-demo"
        action=""
        :on-change="handleImageChange"
        :auto-upload="false"
        :show-file-list="false"
    >
      <el-button type="primary">Загрузить изображение</el-button>
    </el-upload>

    <div v-if="imageUrl" class="image-preview">
      <h4>Предварительный просмотр:</h4>
      <img :src="imageUrl" alt="Загруженное изображение" class="image-preview__img"/>
    </div>

    <el-button
        v-if="imageUrl"
        type="success"
        @click="submitImage"
        style="margin-top: 10px;">
      Отправить
    </el-button>
  </div>
</template>

<script>
import {mapActions} from 'vuex';
import {ROUTES} from "@/router";

export default {
  data() {
    return {
      imageUrl: '',
      selectedFile: null,
      loading: false,
    };
  },
  methods: {
    ...mapActions('table', ['predictData', 'addData']),

    handleImageChange(file) {
      this.selectedFile = file.raw;
      this.imageUrl = URL.createObjectURL(file.raw);
    },

    submitImage() {
      if (!this.selectedFile) {
        this.$message.error('Пожалуйста, выберите изображение.');
        return;
      }

      this.loading = true;

      console.log('Файл для предсказания:', this.selectedFile);

      this.predictData(this.selectedFile)
          .then(response => {

            const predictions = response.data.individual_predictions.map(prediction => String(prediction[0]));
            const ensemble = String(response.data.ensemble_prediction[0]);

            this.addData(
                {
                  image: this.selectedFile.name,  // Используйте имя файла для изображения
                  model1: predictions[0],        // Модели 1, 2 и 3
                  model2: predictions[1],
                  model3: predictions[2],
                  ensemble: ensemble              // Ensemble предсказание
                })
                .then(() => {
                  this.$router.push({name: ROUTES.LIST});
                })
          })
          .finally(() => {
            this.loading = false;
          })
    },
  },
};
</script>

<style lang="less" scoped>
.image-preview {
  margin-top: 20px;
  text-align: center;

  &__img {
    max-height: 400px;
    width: auto;
    border: 1px solid #ddd;
    padding: 5px;
  }
}
</style>