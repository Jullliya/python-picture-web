<template>
  <div class="animated-container" v-loading="loading">
    <div class="table-container">
      <div class="table-container__controls">
        <ElButton type="primary" @click="() => openLoad()">Добавить</ElButton>
        <ElButton type="danger" @click="() => deleteAll()">Удалить все</ElButton>
        <ElButton type="danger" @click="() => logout()">Выход</ElButton>
        <ElDialog
            :visible.sync="isDownloadModalVisible"
            title="Добавить данные"
            width="30%"
            @close="closeDownloadModal"
            class="controls-container__modal-window">
          <ElForm>
            <ElFormItem label="Пациент">
              <ElInput v-model="formData.patient" placeholder="Введите фио пациента"></ElInput>
            </ElFormItem>
            <ElFormItem label="Описание">
              <ElInput v-model="formData.description" type="textarea" placeholder="Введите описание"></ElInput>
            </ElFormItem>
            <ElFormItem>
              <vue-dropzone
                  ref="myDropzone"
                  id="dropzone"
                  :options="dropzoneOptions"
                  @vdropzone-file-added="handleFileAdded"
                  class="controls-container__modal-window--dropzone">
              </vue-dropzone>
            </ElFormItem>
          </ElForm>
          <span slot="footer" class="controls-container__dialog-footer">
          <ElButton @click="closeDownloadModal">Отмена</ElButton>
          <ElButton type="primary" @click="handleSubmit">Сохранить</ElButton>
        </span>
        </ElDialog>
      </div>

      <ElTable class="table-container__table" :data="paginatedData" @row-click="(row) => openModal(row, paginatedData)">
        <ElTableColumn label="Пациент" prop="patient"/>
        <ElTableColumn label="Изображение">
          <template #default="{ row }">
            <img
                class="table-container__table--preview-image"
                :src="row.image"
                alt="Предпросмотр"
            />
          </template>
        </ElTableColumn>
        <ElTableColumn label="Дата и время загрузки" prop="date"/>
        <ElTableColumn label="Модель 1 / Модель 2 / Модель 3 (Ансамбль)">
          <template #default="scope">
            <span>{{ formatModelsAndResult(scope.row) }}</span>
            <i v-if="isResultMatch(scope.row)" class="table-container__result-check el-icon-check"></i>
          </template>
        </ElTableColumn>
        <ElTableColumn label="Действия" class="table-container__actions">
          <template #default="{ $index }">
            <ElButton
                type="danger"
                size="mini"
                @click.stop="() => deleteItem($index)">
              Удалить
            </ElButton>
          </template>
        </ElTableColumn>
        <template #empty>
          <p>Нет данных для отображения. Таблица пустая.</p>
        </template>
      </ElTable>

      <ElDialog
          :visible.sync="isModalVisible"
          title="Результат"
          width="40%"
          @close="() => closeModal()"
          class="table-container__modal-window--image">
        <div v-if="modalTitle">
          <img :src="modalTitle" alt="Изображение"/>
          <div class="modal-probabilities">
            <div class="field">
              <span class="field-label">Вероятность 1 модели:</span>
              <span class="field-value">{{ selectedRow.model_1}} - {{ (parseFloat(selectedRow.model_1_probability) * 100).toFixed(2) }}%</span>
            </div>
            <div class="field">
              <span class="field-label">Вероятность 2 модели:</span>
              <span class="field-value">{{ selectedRow.model_2}} - {{ (parseFloat(selectedRow.model_2_probability) * 100).toFixed(2) }}%</span>
            </div>
            <div class="field">
              <span class="field-label">Вероятность 3 модели:</span>
              <span class="field-value">{{ selectedRow.model_3}} - {{ (parseFloat(selectedRow.model_3_probability) * 100).toFixed(2) }}%</span>
            </div>
            <div class="field">
              <span class="field-label">Вероятность ансамбля:</span>
              <span class="field-value">{{ selectedRow.ensemble}} - {{ (parseFloat(selectedRow.ensemble_probability) / 3 * 100).toFixed(2) }}%</span>
            </div>
          </div>
        </div>
        <div v-else>
          <p>Загрузка изображения...</p>
        </div>
        <div class="modal-fields">
          <div class="field">
            <span class="field-label">Пациент:</span>
            <span class="field-value">{{ patientName }}</span>
          </div>

          <div class="field">
            <span class="field-label">Описание:</span>
            <span class="field-value">{{ description }}</span>
          </div>

          <div class="field">
            <span class="field-label">Диагноз:</span>
            <span class="field-value">{{ getDiagnosisLabel(diagnosis) }}</span>
          </div>
        </div>
        <div slot="footer" class="el-dialog__footer">
          <ElButton @click="() => openEditModal()">Редактировать</ElButton>
          <ElButton @click="() => closeModal()">Закрыть</ElButton>
        </div>
      </ElDialog>
      <ElDialog
          :visible.sync="isEditModalVisible"
          title="Редактирование записи"
          width="40%"
          @close="() => closeEditModal()"
          class="table-container__edit-modal">
        <ElForm>
          <ElFormItem label="Описание">
            <ElInput v-model="editForm.description" type="textarea" placeholder="Введите новое описание"></ElInput>
          </ElFormItem>
          <ElFormItem label="Диагноз">
            <ElSelect v-model="editForm.diagnosis" placeholder="Выберите диагноз">
              <ElOption v-for="option in diagnosisOptions" :key="option.value" :label="option.label"
                        :value="option.value"/>
              <ElOption label="Другое" value="other"/>
            </ElSelect>
          </ElFormItem>
        </ElForm>
        <span slot="footer" class="dialog-footer">
          <ElButton @click="() => closeEditModal()">Отмена</ElButton>
          <ElButton type="primary" @click="() => submitEdit()">Сохранить</ElButton>
        </span>
      </ElDialog>
    </div>
    <div class="animated-container__pagination-container">
      <div class="pagination-container__pagination">
        <ElPagination
            layout="prev, pager, next"
            :current-page="currentPage"
            :page-size="itemsPerPage"
            :total="data.length"
            @current-change="(page)=>changePage(page)">
        </ElPagination>
      </div>
    </div>
  </div>
</template>

<script>
import VueDropzone from 'vue2-dropzone';
import {mapActions} from 'vuex';
import {MessageBox} from 'element-ui';
import {AUTH_TOKEN} from "@/views/LoginView.vue";
import axiosInstance from "@/axios";
import {ROUTES} from "@/router";
import router from "@/router";

export default {
  components: {
    VueDropzone,
  },
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentPage: 1,
      description: '',
      dropzoneOptions: {
        url: '/upload',
        autoProcessQueue: false,
        addRemoveLinks: false,
        maxFiles: 1,
        acceptedFiles: '.jpg, .jpeg',
        dictDefaultMessage: 'Перетащите файл сюда или нажмите для выбора'
      },
      formData: {
        patient: '',
        description: '',
      },
      isDownloadModalVisible: false,
      isModalVisible: false,
      itemsPerPage: 5,
      loading: false,
      modalTitle: '',
      patientName: '',
      uploadedFiles: [],
      isEditModalVisible: false,
      editForm: {
        id: null,
        description: '',
        diagnosis: '',
      },
      diagnosisOptions: [
        {label: 'Актинический кератоз (AK)', value: 'AK'},
        {label: 'Базальноклеточная карцинома (BCC)', value: 'BCC'},
        {label: 'Доброкачественный кератоз (BKL)', value: 'BKL'},
        {label: 'Дерматофиброма (DF)', value: 'DF'},
        {label: 'Меланома (MEL)', value: 'MEL'},
        {label: 'Меланоцитарный невус (NV)', value: 'NV'},
        {label: 'Плоскоклеточный рак (SCC)', value: 'SCC'},
        {label: 'Сосудистое поражение (VASC)', value: 'VASC'},
      ],
    };
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.data.slice(start, end);
    },
    imageUrl() {
      return `${this.axiosInstance.defaults.baseURL}${this.modalTitle}`;
    }
  },
  methods: {
    axiosInstance,
    ...mapActions('table', ['removeData', 'removeAllData', 'predictData', 'fetchData', 'updateRecord']),

    logout() {
      MessageBox.confirm(
          'Вы уверены, что хотите выйти?',
          'Подтверждение выхода',
          {
            confirmButtonText: 'Да',
            cancelButtonText: 'Нет',
            type: 'warning',
          }
      )
          .then(() => {
            localStorage.removeItem(AUTH_TOKEN)
            router.push(ROUTES.LOGIN)
          })
          .catch(() => {
            console.log("Выход отменён")
          });
    },
    formatModelsAndResult(row) {
      return `${row.model_1} / ${row.model_2} / ${row.model_3} (${row.ensemble})`;
    },
    changePage(page) {
      this.currentPage = page;
    },
    deleteItem(index) {
      MessageBox.confirm(
          'Вы уверены, что хотите удалить этот элемент?',
          'Подтверждение удаления',
          {
            confirmButtonText: 'Да',
            cancelButtonText: 'Нет',
            type: 'warning',
          }
      )
          .then(() => {
            const globalIndex = (this.currentPage - 1) * this.itemsPerPage + index;
            const itemToRemove = this.data[globalIndex];
            this.removeData(itemToRemove.id);
          })
          .catch(() => {
            console.log('Удаление отменено.');
          });
    },
    deleteAll() {
      MessageBox.confirm(
          'Вы уверены, что хотите удалить все?',
          'Подтверждение удаления',
          {
            confirmButtonText: 'Да',
            cancelButtonText: 'Нет',
            type: 'warning',
          }
      )
          .then(() => {
            console.log("Удаление подтверждено.");
            this.removeAllData();
          })
          .catch(() => {
            this.$message.info('Удаление отменено.');
          });
    },
    openLoad() {
      this.isDownloadModalVisible = true;
    },
    handleFileAdded(file) {
      console.log('Файл добавлен:', file);
      this.uploadedFiles = [file];

      setTimeout(() => {
        const successMarks = document.querySelectorAll('.dz-success-mark');
        const errorMarks = document.querySelectorAll('.dz-error-mark');
        successMarks.forEach(mark => mark.remove());
        errorMarks.forEach(mark => mark.remove());
      }, 0);
    },
    handleSubmit() {
      console.log('Данные, полученные из формы:');
      console.log('Файл:', this.uploadedFiles[0]);
      console.log('Пациент:', this.formData.patient);
      console.log('Описание:', this.formData.description);

      if (this.uploadedFiles.length === 0) {
        this.$message.error('Пожалуйста, загрузите изображение.');
        return;
      }

      if (!this.formData.patient || !this.formData.description) {
        this.$message.error('Пожалуйста, заполните все поля.');
        return;
      }

      this.loading = true;

      this.predictData({
        selectedFile: this.uploadedFiles[0],
        patient: this.formData.patient,
        description: this.formData.description
      })
          .then(() => {
            this.$message.success('Данные успешно отправлены и обработаны!');
          })
          .catch(error => {
            console.error('Ошибка предсказания:', error);
            this.$message.error('Ошибка при выполнении предсказания.');
          })
          .finally(() => {
            this.loading = false;
          });

      this.isDownloadModalVisible = false;
      this.uploadedFiles = [];
      this.formData = [];
      this.$refs.myDropzone.removeAllFiles();
    },
    closeDownloadModal() {
      this.isDownloadModalVisible = false;
      this.uploadedFiles = [];
      this.formData = [];
      this.$refs.myDropzone.removeAllFiles();
    },
    openModal(row) {
      this.isModalVisible = true;
      this.modalTitle = row.image;
      this.patientName = row.patient;
      this.description = row.description;
      this.diagnosis = row.diagnosis;
      this.selectedRow = {
        ...row,
        model_1: row.model_1 || "Нет данных",
        model_2: row.model_2 || "Нет данных",
        model_3: row.model_3 || "Нет данных",
        ensemble: row.ensemble || "Нет данных",
        model_1_probability: row.model_1_probability || 0,
        model_2_probability: row.model_2_probability || 0,
        model_3_probability: row.model_3_probability || 0,
        ensemble_probability: row.ensemble_probability || 0
      };
    },
    closeModal() {
      this.isModalVisible = false;
    },
    openEditModal() {
      this.closeModal();
      this.isEditModalVisible = true;
      this.editForm.id = this.selectedRow.id;
      this.editForm.description = this.selectedRow.description;
      this.editForm.diagnosis = this.selectedRow.diagnosis;
    },
    closeEditModal() {
      this.isEditModalVisible = false;
      this.isModalVisible = true;
    },
    submitEdit() {
      if (!this.editForm.description || !this.editForm.diagnosis) {
        this.$message.error('Пожалуйста, заполните все поля.');
        return;
      }

      this.updateRecord(this.editForm)
          .then(() => {
            this.$message.success('Запись успешно обновлена!');

            this.description = this.editForm.description;
            this.diagnosis = this.editForm.diagnosis;

            if (this.selectedRow && this.selectedRow.id === this.editForm.id) {
              this.selectedRow.description = this.editForm.description;
              this.selectedRow.diagnosis = this.editForm.diagnosis;
            }

            this.closeEditModal();
          })
          .catch((error) => {
            console.error('Ошибка при обновлении записи:', error);
            this.$message.error('Ошибка при обновлении записи.');
          });
    },
    getDiagnosisLabel(value) {
      const option = this.diagnosisOptions.find(option => option.value === value);
      return option ? option.label : value;
    },
    isResultMatch(row) {
      return row.ensemble === row.diagnosis;
    },
  },
};
</script>


<style lang="less">
.modal-fields {
  margin-top: 20px;

  .field {
    margin-bottom: 10px;
    font-size: 14px;
    color: #333;

    .field-label {
      font-weight: bold;
      margin-right: 5px;
      display: inline-block;
    }

    .field-value {
      color: #666;
    }
  }
}

.controls-container__modal-window--dropzone {
  background-color: rgba(192, 192, 192, 0.7);
  border: #ccc;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: rgba(192, 192, 192, 1);
  }
}

img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.animated-container__pagination-container {

  &__pagination {
    display: flex;
    justify-content: center;
    text-align: center;
    margin-top: 20px;
  }
}

.table-container {
  margin: 20px;
  text-align: end;

  &__header {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
  }

  &__controls {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    text-align: center;
  }

  &__table {
    width: 100%;

    &--preview-image {
      width: 50px;
      height: 50px;
      object-fit: cover;
      border: 1px solid #ddd;
      padding: 2px;
      border-radius: 4px;
    }


    .el-table__row {
      .el-table__cell:last-child {
        text-align: right;
      }
    }
  }

  &__result-check {
    color: green;
    font-size: 20px;
    margin-left: 8px;
    vertical-align: middle;
  }

  &__modal-window {
    &--image {
      &__header {
        text-align: center;
      }

      padding: 10px;
      box-sizing: border-box;
      overflow: hidden;
    }
  }

  .el-dialog {
    &__header{
      text-align: center;
      font-size: 18px;
      font-weight: bold;
    }
  }
}
.modal-probabilities {
  margin-top: 20px;

  .field {
    margin-bottom: 10px;
    font-size: 14px;

    .field-label {
      font-weight: bold;
      margin-right: 5px;
    }

    .field-value {
      color: #666;
    }
  }
}

</style>