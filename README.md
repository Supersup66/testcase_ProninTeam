### Задача:

Необходимо разработать SPA (Single Page Application) на Vue.js для организации сбора денежных средств. Основная функциональность приложения сводится к созданию нового сбора средств, просмотру существующих кампаний и оплате взносов.

Функционал приложения:

Авторизация осуществляется на стороне сервера, приложение запрашивает токены аутентификации и сохраняет их в браузере.
Пользователь видит главную страницу с кнопкой "Создать сбор" и списком активных кампаний.
При выборе кампании открывается подробная информация о сборе с возможностью оплаты взноса.
Оплата производится путем ввода суммы и отправки POST-запроса на бэкэнд.

Описание Endpoints API:

GET /collections/ — Получение списка всех кампаний.
POST /collections/ — Создание новой кампании.
GET /collections/{pk}/ — Детали конкретной кампании.
POST /collections/{pk}/payments/ — Отправка платежа.

Архитектура проекта:

Главная страница (Home.vue):

Отображение списка кампаний.
Кнопка "Создать сбор".


Создание новой кампании (CreateCollection.vue):

Форма для заполнения полей: причина сбора, название, описание, целевая сумма, срок окончания.


Просмотр деталей кампании (CollectionDetail.vue):

Информация о кампании (автор, собранная сумма, количество участников, цель, сроки).
Возможность внести платеж.


Оплата взноса (PaymentModal.vue):

Модальное окно для ввода суммы платежа и подтверждения транзакции.

Проектирование файлового дерева:

src/
|- components/
|   |- CollectionItem.vue       // Компонент для каждого элемента списка кампаний
|   |- PaymentModal.vue         // Модальное окно для внесения платежей
|
|- layouts/
|   |- DefaultLayout.vue        // Базовый макет для приложения
|
|- pages/
|   |- Home.vue                // Главная страница
|   |- CreateCollection.vue    // Страница создания новой кампании
|   |- CollectionDetail.vue    // Подробности одной кампании
|
|- services/
|   |- apiService.js           // Сервис для взаимодействия с API
|
|- store/
|   |- auth.js                 // Логика авторизации
|   |- collections.js          // Управление состоянием кампаний
|
|- router.js                  // Настройки роутинга
|- main.js                    // Точка входа приложения
|- App.vue                    // Главный контейнер приложения

Пример реализации компонентов:

components/CollectionItem.vue

Отображает элемент списка кампаний:
```
<template>
  <div class="collection-item">
    <h3>{{ collection.title }}</h3>
    <p>Автор: {{ collection.author.username }}</p>
    <p>Описание: {{ collection.description }}</p>
    <router-link :to="'/collections/' + collection.id">Подробнее</router-link>
  </div>
</template>

<script>
export default {
  props: ['collection'],
};
</script>
```
pages/Home.vue

Основная страница с отображением списка кампаний и кнопкой создания новой кампании:
```
<template>
  <DefaultLayout>
    <h1>Список кампаний:</h1>
    <ul v-if="collections.length > 0">
      <li v-for="collection in collections" :key="collection.id">
        <CollectionItem :collection="collection"/>
      </li>
    </ul>
    <button @click="createNewCollection">Создать новый сбор</button>
  </DefaultLayout>
</template>

<script>
import { mapState } from 'vuex';
import CollectionItem from '@/components/CollectionItem.vue';

export default {
  components: { CollectionItem },
  computed: mapState(['collections']),
  methods: {
    async fetchCollections() {
      await this.$store.dispatch('fetchCollections');
    },
    createNewCollection() {
      this.$router.push('/create');
    },
  },
  created() {
    this.fetchCollections();
  },
};
</script>
```
services/apiService.js

Сервис для взаимодействия с REST API:
```
import axios from 'axios';

const BASE_URL = process.env.VUE_APP_API_BASE_URL || '/api/';

export const apiService = {
  async getCollections() {
    try {
      const response = await axios.get(`${BASE_URL}v1/collections`);
      return response.data;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },

  async createCollection(data) {
    try {
      const response = await axios.post(`${BASE_URL}v1/collections`, data);
      return response.data;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },

  async getCollectionDetails(id) {
    try {
      const response = await axios.get(`${BASE_URL}v1/collections/${id}`);
      return response.data;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },

  async makePayment(collectionId, paymentData) {
    try {
      const response = await axios.post(
        `${BASE_URL}v1/collections/${collectionId}/payments`,
        paymentData
      );
      return response.data;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
};
```
store/index.js

Хранилище состояний (Vuex):
```
import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import collections from './modules/collections';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    collections,
  },
});
```
store/modules/collections.js

Логика хранения и обработки кампаний:
```
import { apiService } from '@/services/apiService';

const state = () => ({
  collections: [],
});

const mutations = {
  SET_COLLECTIONS(state, payload) {
    state.collections = payload;
  },
};

const actions = {
  async fetchCollections({ commit }) {
    const collections = await apiService.getCollections();
    commit('SET_COLLECTIONS', collections);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
```
Роуты (router.js):
```
import VueRouter from 'vue-router';
import Home from '@/pages/Home.vue';
import CreateCollection from '@/pages/CreateCollection.vue';
import CollectionDetail from '@/pages/CollectionDetail.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/create', component: CreateCollection },
  { path: '/collections/:id', component: CollectionDetail },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
```
Запуск приложения:

Запустить приложение можно стандартным способом:

npm install
npm run serve

Итог:

Теперь у тебя есть полное представление о структуре приложения, взаимодействии с API и работе с основными компонентами. Данный каркас можно расширять дополнительными возможностями, такими как улучшенная навигация, обработка ошибок, улучшение UX-интерфейса и интеграция сторонних сервисов для оплаты.