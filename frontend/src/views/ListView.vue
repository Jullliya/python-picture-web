<template>
  <div class="list">
    <h1>Анализ</h1>
    <TableComponent :data="tableData"/>
  </div>
</template>

<script>
import TableComponent from '@/components/TableComponent.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'ListVue',
  components: {
    TableComponent,
  },
  computed: {
    ...mapGetters('table', ['getTableData']),
    tableData() {
      return this.getTableData;
    },
  },
  created() {
    this.$store.dispatch('table/fetchTableData');
  },
};
</script>