<template>
    <h1 v-if="lesson_data != null" class="h1-in-lesson">{{ `${lesson_data.subject.title}, ${lesson_data.group.title}` }}
    </h1>
    <h2 v-if="lesson_data != null">{{ `${lesson_data.date}, ${lesson_data.order_in_day}-я пара` }}</h2>
    <div v-if="lesson_data != null & ranks != null & students != null">
        <!-- <p>{{ total_data }}</p> -->
        <div v-for="(data, index) in total_data" class="student-in-list-div">
            <h3>{{ `${data.lastname} ${data.firstname}` }}</h3>
            <div class="student-in-list-input-div">
                <label for="student-visit-checkbox">Посещение: <input type="checkbox" name="student-visit-checkbox"
                        id="student-visit-checkbox" v-model="total_data[index].visited"></label>
                <br>
                <label for="student-rank-input">Оценка: <input v-model="total_data[index].rank" type="number" min="2"
                        max="5" name="student-rank-input" id="student-rank-input"></label>
            </div>
        </div>
    </div>
    <button class="default-button">Сохранить</button>
</template>

<script>
import { getStudentsByGroup } from '@/network';
import { getLesson } from '@/network';
import { getRanksForLesson } from '@/network';
import router from '@/router';
import { getDayOfWeek } from '@/service';
import swal from 'sweetalert';

export default {
    data() {
        return {
            lesson_data: null,
            ranks: null,
            students: null,
            total_data: []
        }
    },
    methods: {

    },
    async created() {
        const id = this.$route.params.id;
        this.id = id;
        if (Number.isInteger(+id)) {
            this.lesson_data = await getLesson(id);
            this.ranks = await getRanksForLesson(id);
            this.students = await getStudentsByGroup(this.lesson_data.group.title);

            let student_id;
            let student_lastname;
            let student_firstname;
            let visited;
            let student_rank;
            let new_student;

            this.students.forEach(student => {
                student_id = student.id;
                student_lastname = student.lastname;
                student_firstname = student.firstname;
                visited = false;
                student_rank = null;
                this.lesson_data.visits.forEach(visit => {
                    if (student.id == visit.id) {
                        visited = true;
                    }
                });
                this.ranks.forEach(rank => {
                    if (student.id == rank.student.id) {
                        student_rank = rank.rank;
                    }
                });
                new_student = {
                    "id": student_id,
                    "lastname": student_lastname,
                    "firstname": student_firstname,
                    "visited": visited,
                    "rank": student_rank,
                };
                this.total_data.push(new_student);
            });
        }
        else {
            // swal
            // router.replace('/')
        }

    }
}

</script>

<style>
.h1-in-lesson {
    margin: 17px 0;
}

.student-in-list-div {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
    padding: 5px 0 25px 30px;
    background-color: var(--dpurple);
    border-radius: 8px;
    min-width: 60vw;
}

.student-in-list-input-div {
    display: flex;
    flex-direction: column;
}
</style>
