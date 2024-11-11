<template>
  <div class="table-container">
    <ElTable class="table-container__table" :data="paginatedData">
      <ElTableColumn label="Изображение" prop="image"/>
      <ElTableColumn label="Модель 1" prop="model_1"/>
      <ElTableColumn label="Модель 2" prop="model_2"/>
      <ElTableColumn label="Модель 3" prop="model_3"/>
      <ElTableColumn label="Результат" prop="ensemble"/>
      <ElTableColumn label="Действия">
        <template #default="{ $index }">
          <ElButton
              type="danger"
              size="mini"
              @click="() => deleteItem($index)">
            Удалить
          </ElButton>
        </template>
      </ElTableColumn>
    </ElTable>

    <div class="table-container__pagination">
      <ElPagination
          layout="prev, pager, next"
          :current-page="currentPage"
          :page-size="itemsPerPage"
          :total="data.length"
          @current-change="(page)=>changePage(page)">
      </ElPagination>
    </div>
    <div class="table-container__bottom">
      <ElButton type="primary" @click="() => loadMore()">Добавить</ElButton>
    </div>
  </div>
</template>

<script>
import {mapActions} from 'vuex';
import {ROUTES} from "@/router";

export default {
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 5,
    };
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.data.slice(start, end);
    },
  },
  methods: {
    ...mapActions('table', ['removeData']),
    changePage(page) {
      this.currentPage = page;
    },
    deleteItem(index) {
      const globalIndex = (this.currentPage - 1) * this.itemsPerPage + index;
      const itemToRemove = this.data[globalIndex];
      this.removeData(itemToRemove.id);

      if (this.data.length === 0) {
        this.$router.push({name: ROUTES.HOME});
      }
    },
    loadMore() {
      this.$router.push({name: ROUTES.HOME});
    }
  },
};
</script>

<style scoped>
.table-container {
  margin: 20px;

  &__header {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
  }

  &__table {
    width: 100%;
  }

  &__pagination {
    margin-top: 10px;
    display: flex;
    justify-content: center;
  }
}
</style>