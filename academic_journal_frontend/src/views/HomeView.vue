<script>
import { tokenIsSet } from '../service';

export default {
  data() {
    return {
      username: null,
      isAuth: null
    }
  },
  created() {
    // this.isAuth = tokenIsSet();
    if (tokenIsSet()) {
      this.isAuth = true;
      this.username = localStorage.getItem('username');
      this.first_name = localStorage.getItem('first_name');
      this.last_name = localStorage.getItem('last_name')
    }
    else {
      this.isAuth = false;
    }
  }
}

</script>

<template>
  <div v-if="isAuth === true">
    <h1>Добро пожаловать, {{ last_name }} {{ first_name }}!</h1>
  </div>
  <div v-if="isAuth === false">
    <h1 class="test">Добро пожаловать!</h1>
    <h2 class="test">Зарегистрируйтесь или авторизуйтесь для начала работы с журналом!</h2>
  </div>
  <!-- <main>
    <p>kek</p>
  </main> -->
</template>

<style scoped>
  .test {
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  }
  h1 {
    -webkit-text-stroke: 2.5px var(--black);
    font-size: 56px;
  }
  h2 {
    -webkit-text-stroke: 1.5px var(--black);
    font-size: 35px;
  }
</style>