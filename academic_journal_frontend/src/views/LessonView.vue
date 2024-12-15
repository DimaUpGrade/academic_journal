<template>
    <h1 v-if="lesson_data != null" class="h1-in-lesson">{{ `${lesson_data.subject.title}, ${lesson_data.group.title}` }}
    </h1>
    <h2 v-if="lesson_data != null">{{ `${lesson_data.date}, ${lesson_data.order_in_day}-я пара` }}</h2>
    <div v-if="lesson_data != null & ranks != null & students != null">
        <!-- <p>{{ total_data }}</p> -->
        <div v-for="(data, index) in total_data" class="student-in-list-div">
            <h3>{{ `${data.lastname} ${data.firstname}` }}</h3>
            <div class="student-in-list-input-div">
                <label v-bind:for="`student-visit-checkbox-${index}`">Посещение: <input
                        v-model="total_data[index].visited" v-bind:id="`student-visit-checkbox-${index}`"
                        v-bind:name="`student-visit-checkbox-${index}`" type="checkbox"></label>
                <br>
                <label v-bind:for="`student-rank-input-${index}`">Оценка: <input v-model="total_data[index].rank"
                        v-bind:id="`student-rank-input-${index}`" v-bind:name="`student-rank-input-${index}`"
                        type="number" min="2" max="5"></label>
            </div>
        </div>
    </div>
    <button class="default-button" @click="saveChanges">Сохранить</button>
</template>

<script>
import { getStudentsByGroup } from '@/network';
import { getLesson } from '@/network';
import { getRanksForLesson } from '@/network';
import { postRanks } from '@/network';
import { postVisits } from '@/network';
import router from '@/router';
import { getDayOfWeek } from '@/service';
import swal from 'sweetalert';

export default {
    data() {
        return {
            id: null,
            lesson_data: null,
            ranks: null,
            students: null,
            total_data: []
        }
    },
    methods: {
        async saveChanges() {
            let ranks = [];
            let visits = [];
            let student_rank = null;
            let student_visit = null;

            this.total_data.forEach(element => {
                student_rank = {
                    'lesson_id': this.id,
                    'student_id': element.id,
                    'rank': element.rank,
                };
                ranks.push(student_rank);

                student_visit = {
                    'student_id': element.id,
                    'visited': element.visited
                }
                visits.push(student_visit);
            });

            await postRanks(ranks);
            await postVisits(visits, this.id)

            swal({
                title: "Данные сохранены!",
                text: "Вы будете перенаправлены на страницу журнала!",
                type: "success"
            }).then(function () {
                router.back();
            });
        }
    },
    async created() {
        const id = this.$route.params.id;
        this.id = id;
        if (Number.isInteger(+id)) {
            this.id = Number(this.id);
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
