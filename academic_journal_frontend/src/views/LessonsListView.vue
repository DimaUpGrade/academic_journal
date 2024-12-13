<template>
    <div>
        <h1>Академический журнал</h1>
        <h2>{{ `${subject}, ${group}` }}</h2>
        <br>
        <h3 v-if="lessons != null" v-for="lesson in lessons" @click="goToLesson(lesson.id)" class="lesson-title-in-list">{{ `Занятие от ${lesson.date}, ${getDayOfWeekMethod(lesson.date)}` }}</h3>
    </div>
</template>

<script>
import router from '@/router';
import { getLessons } from '@/network';
import { getDayOfWeek } from '@/service';

    export default {
        data() {
            return {
                group: null,
                subject: null,
                semester_id: null,
                lessons: null
            }
        },
        methods: {
            goToLesson(id) {
                router.push(`/lessons/${id}`);
            },
            getDayOfWeekMethod(date) {
                return getDayOfWeek(date);
            }
        },
        async created() {
            this.group = this.$route.query.group;
            this.subject = this.$route.query.subject;
            this.semester_id = this.$route.query.semester;

            if (this.group == null | this.subject == null | this.semester_id == null) {
                router.replace("/")
            }

            this.lessons = await getLessons(this.group, this.subject, this.semester_id)
        }
    }
</script>

<style scoped>
    .lesson-title-in-list {
        color: var(--white-smoke);
        font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        -webkit-text-stroke: 1.1px var(--black);
        font-size: 25px;
        text-decoration: underline;
        text-decoration-color: var(--white-smoke);
         
    }

    .lesson-title-in-list:hover {
        cursor: pointer;
        color: var(--black);
        -webkit-text-stroke: 0px;
        text-decoration-color: var(--black);
    }
</style>