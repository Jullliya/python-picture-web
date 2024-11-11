import axiosInstance from "@/axios";

const state = {
    tableData: [],
};

const mutations = {
    SET_TABLE_DATA(state, data) {
        state.tableData = data;
    },
};

const actions = {
    fetchData({commit}) {
        const authToken = localStorage.getItem('authToken')
        return axiosInstance.get(`cnn_table/${authToken}/get`)
            .then((response) => {
                commit('SET_TABLE_DATA', response.data);
            })
            .catch(error => {
                console.error('Ошибка при получении данных:', error);
            });
    },
    addData({dispatch}, {image, model1, model2, model3, ensemble}
    ) {
        const authToken = localStorage.getItem('authToken')
        return axiosInstance
            .post(`/cnn_table/${authToken}/add`, {}, {
                params: {
                    image: String(image),
                    model_1: String(model1),
                    model_2: String(model2),
                    model_3: String(model3),
                    ensemble: ensemble.toString(),
                }
            })
            .then(() => {
                dispatch('fetchData');
            })
            .catch((error) => {
                console.error('Ошибка при записи в таблицу:', error);
            });
    },
    // eslint-disable-next-line no-unused-vars
    predictData({ commit },selectedFile) {
        const formData = new FormData();
        formData.append('image', selectedFile);

        return axiosInstance.post('/back/classification-image', formData)
            .catch(error => {
                console.error('Ошибка при загрузке изображения:', error);
            });
    },
    removeData({dispatch}, index) {
        const authToken = localStorage.getItem('authToken')

        return axiosInstance.get(`/cnn_table/${authToken}/delete`, {
            params: { id: index }
        })
            .then(() => {
                dispatch('fetchData');
            })
            .catch(error => {
                console.error('Ошибка при удалении данных:', error);
            });
    },
};

const getters = {
    getTableData: (state) => state.tableData,
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};
