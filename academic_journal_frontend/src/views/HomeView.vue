<script>
import { tokenIsSet } from '../service';
import { getSubjects } from '@/network';
import { getSemesters } from '@/network';
import { getGroups } from '@/network';
import router from '@/router';

import swal from 'sweetalert';

export default {
  data() {
    return {
      username: null,
      isAuth: null,
      first_name: null,
      last_name: null,
      groups: null,
      subjects: null,
      semesters: null,
      chosen_group: null,
      chosen_subject: null,
      chosen_semester: null
    }
  },
  methods: {
    openJournal() {
      if (this.chosen_group != null & this.chosen_subject != null & this.chosen_semester != 0) {
        router.push({path: `/lessons/`, query: {group: this.chosen_group, subject: this.chosen_subject, semester: this.chosen_semester}})
      }
      else {
        swal({
          title: "Ошибка!",
          text: "Заполните все обязательные поля!",
          type: "success"
        }).then(function () { });
      }
    }
  },
  async created() {
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

    this.groups = await getGroups();
    this.subjects = await getSubjects();
    this.semesters = await getSemesters();
  }
}

</script>

<template>
  <div v-if="isAuth === false">
    <h1 class="test">Добро пожаловать!</h1>
    <h2 class="test">Зарегистрируйтесь или авторизуйтесь для начала работы с журналом!</h2>
  </div>
  <div>
    <h1 v-if="isAuth === true">Добро пожаловать, {{ last_name }} {{ first_name }}!</h1>
    <div id="lesson-search-display" v-if="groups != null & subjects != null & semesters != null">
      <h2>Чтобы перейти к занятиям группы, укажите предмет, группу и семестр</h2>

      <label for="group-choice">Выберите группу:</label>
      <input v-model="chosen_group" list="group-list" id="group-choice" name="group-choice" class="input-chooser">
      <datalist name="group-list" id="group-list" v-if="groups != null">
        <option v-for="group in groups" v-bind:value="group.title">{{ group.title }}</option>
      </datalist>

      <label for="subject-choice">Выберите предмет:</label>
      <input v-model="chosen_subject" list="subject-list" id="subject-choice" name="subject-choice"
        class="input-chooser">
      <datalist name="subject-list" id="subject-list">
        <option v-for="subject in subjects" v-bind:value="subject.title">{{ subject.title }}</option>
      </datalist>

      <label for="semester-choice">Выберите семестр:</label>
      <input v-model="chosen_semester" list="semester-list" id="semester-choice" name="semester-choice"
        class="input-chooser">
      <datalist name="semester-list" id="semester-list">
        <option v-for="semester in semesters" v-bind:value="semester.id">{{ semester.start_year + '-' +
          semester.end_year + ' гг., ' + semester.semester_number + '-й семестр' }}</option>
        <!-- v-bind:label="semester.start_year + '-' + semester.end_year + ' гг., ' + semester.semester_number + '-й семестр'" -->
      </datalist>

      <button class="default-button" @click="openJournal">Открыть журнал</button>
    </div>
  </div>

  <!-- <main>
    <p>kek</p>
  </main> -->
</template>

<style scoped>
.test {
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

h1 {
  -webkit-text-stroke: 2.5px var(--black);
  font-size: 56px;
}

h2 {
  -webkit-text-stroke: 1.5px var(--black);
  font-size: 35px;
}

#lesson-search-display {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: start;
  justify-content: center;
  gap: 8px;
}

.input-chooser {
  min-width: 400px;
}
</style>