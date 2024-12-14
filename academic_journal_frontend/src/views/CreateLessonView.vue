<template>
    <h1>Создание занятия</h1>
    <div class="default-center-div">
        <div class="default-start-div">
            <label for="lesson-date-input">Укажите дату занятия:</label>
            <input v-model="date" type="date" name="lesson-date-input" id="lesson-date-input">
        </div>
        <div class="default-start-div">
            <label for="lesson-order-in-day-input">Укажите номер пары:</label>
            <select v-model="order_in_day" name="lesson-order-in-day-input" id="lesson-order-in-day-input">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="6">7</option>
                <option value="6">8</option>
                <option value="6">9</option>
            </select>
        </div>

        <button class="default-button" @click="createLessonMethod">Создать занятие</button>
    </div>
</template>

<script>
import { tokenIsSet } from '@/service';
import { createLesson } from '@/network';
import router from '@/router';
import swal from 'sweetalert';

// взять из квери-параметров группу, предмет, семестр
export default {
    data() {
        return {
            group: null,
            subject: null,
            semester_id: null,
            date: null,
            order_in_day: null,
        }
    },
    methods: {
        async createLessonMethod() {
            if (this.date != null & this.order_in_day != null) {
                await createLesson(this.date, this.order_in_day, this.group, this.subject, this.semester_id);
            }
            else {
                swal({
                    title: "Ошибка!",
                    text: "Проверьте правильность заполнения полей!",
                    type: "success"
                }).then();
            }
        }
    },
    created() {
        if (!tokenIsSet()) {
            router.replace("/")
        }

        this.group = this.$route.query.group;
        this.subject = this.$route.query.subject;
        this.semester_id = this.$route.query.semester;

        if (this.group == null | this.subject == null | this.semester_id == null) {
            router.replace("/")
        }
    }
}
</script>

<style></style>