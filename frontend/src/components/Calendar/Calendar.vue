<template>
<v-container>
    <!-- filter / controller -->
    <v-row align-center class="filter">
        <v-col >
            <v-select
            item-text="text"
            itme-value="value"
            :items="viewModeOptions"
            v-model="selectedView.value"
            label="View Type"
            outlined
            ></v-select>
        </v-col>

        <v-col>
                <v-btn type="button" class="btn elevation-0" @click="to('today')">Today</v-btn>
                <v-btn type="button" class="btn elevation-0" @click="to('prev')">Prev</v-btn>
                <v-btn type="button" class="btn elevation-0" @click="to('next')">Next</v-btn>
        </v-col>
    </v-row>
    <!-- Calendar -->
    <v-row>
        <v-col cols="12">
    
            <Calendar
            ref="tuiCalendar"
            :view="selectedView.value"
            :calendars="calendarList"
            :schedules="scheduleList"
            :theme="themeConfig"
            :useCreationPopup="false"
            :useDetailPopup="false"

            @afterRenderSchedule="onAfterRenderSchedule"
            @beforeCreateSchedule="onBeforeCreateSchedule"
            @beforeDeleteSchedule="onBeforeDeleteSchedule"
            @beforeUpdateSchedule="onBeforeUpdateSchedule"
            @clickDayname="onClickDayname"
            @clickSchedule="onClickSchedule"
            @clickTimezonesCollapseBtn="onClickTimezonesCollapseBtn"
            />
        </v-col>
    </v-row>

    <!-- slot을 이용해 내용을 정의하는 방법 https://goddino.tistory.com/93 -->
    <AddEventModal
        :calendarGroups="privateCalendars"
        :dialog="dialog"
        :default_date="default_date"
        :schedule="schedule"
        @_dialog="setDialog"
        @newEvent="addNewEvent"
        @newGroup="addNewGroup"/>
    <SchduleDetailModal 
    v-if="open" 
    :event="now_event" 
    @updateEvent="updateEvent"
    @deleteEvent="deleteEvent"/>
    <!-- Add Private Event Type Modal -->
    
</v-container>
</template>
<script>
import 'tui-calendar/dist/tui-calendar.css'
import { Calendar } from '@toast-ui/vue-calendar';

// If you use the default popups, use this.
import 'tui-date-picker/dist/tui-date-picker.css';
import 'tui-time-picker/dist/tui-time-picker.css';
import themeConfig from './myTheme.js'

import axios from "axios";
import setToken from "../../js_utils/token.js"

import AddEventModal from './AddEvent.vue'
import SchduleDetailModal from './ScheduleDetail.vue'

let url = "http://127.0.0.1:8000/api/wrapper/";

export default {
    data : () => {

        
      return {
            // calendar configurations
            themeConfig : themeConfig,
            events : [],
            calendarList: [

            ],
            scheduleList: [],

            //scheduleList: [],
            selectedView: {
                    text : 'Monthly',
                    value : 'month'
            },
            viewModeOptions: [
                { text : 'Monthly', value : 'month' },
                { text : 'Weekly', value : 'week' },
                {text : 'Daily', value : 'day' }
            ],

            // event modal
            dialog: false, // control modal on/off
            default_date : "",
            schedule : "",

            // schedule detail modal
            now_event : "",
            open : false
            }  
    },

    methods : {
        setDate : function(){
            return (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
        },

        parseEvent : function(data, index){

            let event = data.event
            console.log(data)
            let attendees = event.relatedPeople

            return {
                    id: event.id,
                    calendarId: String(event.group.id),//String(event.group), // undefined
                    title: event.title,
                    category: 'allday',
                    dueDateClass: '',
                    start: event.start,
                    end: event.end,
                    body : event.description,
                    isPrivate : event.group.is_private,
                    attendees : attendees,
                    raw : {
                        author : String(event.author),
                        wrapper_id : data.id,
                        index : index
                    }
                }

        },

        parseGroup : function(eventgroup) {
            console.log(eventgroup)
                eventgroup.id = String(eventgroup.id)
                eventgroup.bgColor = eventgroup.color
                eventgroup.borderColor = eventgroup.color
                delete eventgroup.color   

                return eventgroup
        },

        to : function(direction) {  
            this.$refs.tuiCalendar.invoke(direction); // ~invoke : tui calendar의 method를 call하기 위한 방법임. 
        },
        // http://forward.nhnent.com/hands-on-labs/toastui.calendar-timetable/05%20events.html#id2

        setDialog : function(dialog) {
            this.dialog = false
            this.schedule = ""
        },

        deleteEvent : function(index){
            this.scheduleList.splice(index, 1)
        },

        addNewEvent : function(newEvent){
            if (newEvent.index !== -1){
                this.deleteEvent(newEvent.index)
            }

            this.scheduleList.push( this.parseEvent(newEvent.data) )
        },

        addNewGroup : function(newGroup){
            this.calendarList.push( this.parseGroup(newGroup) )
        },

        updateEvent : function(schedule){
            this.schedule = schedule
            this.dialog = true
            
        },

        onAfterRenderSchedule(e) {
            // 캘린더 전체를 렌더링한 이후 매 싱글 스케쥴에 적용됨
            let schedule = e.schedule;
            // use the element
        },
        onBeforeCreateSchedule(e) {
            // calendar cell 클릭하면 발생
            this.default_date = e.start._date.toISOString().substr(0, 10)
            
            this.dialog = true
            // let the creation guide invisible
            let guide = e.guide;
            guide.clearGuideElement();

            // 그냥 스케쥴 추가 버튼으로 여는게 제일 좋아보임
            // 
            
        },
        
        AddPrivateSchdule : function(){
            // axios로 private schedule 추가
            // 잘 추가 됐으면 해당 schedule을 schedules에 푸시
        },


        onBeforeDeleteSchedule(e) {
            // 스케쥴 삭제 시 이 이벤트
            console.log('schedule delete')
            
        },
        onBeforeUpdateSchedule(e) {
            // view type을 바꾸기 위해 스케쥴을 드래그 할 때 발생 > drag은 끌거임
            console.log('update')
            
        },
        onClickDayname(e) {
            // weekly view에서 day name을 클릭했을 때 
            console.log('day name click')
            
        },
        onClickSchedule(e) {
            // schedule을 클릭했을 때 발생
            // 툴팁 팝업 띄우고
            // private이면 삭제 / 수정 가능하게
            

            // 누르면 x, y 좌표 받고
            // 열어 새끼야
            // 좌표 말고 e.schedule이 바뀔 때 여는거 아님?
            

            
            //this.openTooltip = true
            //console.log(this.openTooltip)
            //this.tooltip_x = e.event.pageX
            //this.tooltip_y = e.event.pageY
            this.now_event = e
            this.open = true
            console.log(this.now_event)
        },
        onClickTimezonesCollapseBtn(e) {
            // tz collapse 버튼을 눌렀을 때
            console.log('tz collapse') 


        },
        reopen : function(reopen){
            this.close()
            this.open() 
        },

        close : function(close){
            this.openTooltip = false
        },
        // open : function(){
        //     this.openTooltip = true
        // },


        },


    components: {
        Calendar,
        AddEventModal,
        SchduleDetailModal
    },

    mounted() {

        axios({
            method : "GET",
            url : url,
            headers : setToken(),
            params : {
                content_type : "event",
                view_type : "calendar",
                user_id : localStorage.getItem('user')
            }
        })
        .then((response) => {
            console.log('response', response)
            let data = response.data.data
            let eventgroups = response.data.eventgroups

            for (let i in data){
                this.scheduleList.push(this.parseEvent(data[i], i))
            }

            for (let i in eventgroups){
                this.calendarList.push(this.parseGroup(eventgroups[i]))
           }




        })
        .catch(response => {
            console.log("Failed", response);
        });

    },

    computed: {
        privateCalendars : function(){
            let arr = Array()
            for (let i in this.calendarList){
                if (this.calendarList[i].is_private === true){
                    arr.push(this.calendarList[i])
                }
            }

            return arr
        }

    }



}
</script>


<style scoped>
    .btn{
        padding-top:5px;
        padding-bottom:5px;
        padding-left: 15px;
        padding-right: 15px;
        margin: 5px;
        border-radius: 30px;
        background-color: #ffffff!important;
        border-color: #DCDCDC!important;
        border:solid 1px;
    }

    .filter{
        margin-bottom:-50px;
    }

</style>