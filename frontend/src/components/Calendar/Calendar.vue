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
            <v-btn
            class="mx-2"
            fab
            color="indigo"
            
            >
                <v-icon>
                    mdi-plus
                </v-icon>
            </v-btn>
        </v-col>
    </v-row>

    <!--Add Private Event Modal-->
    <v-row justify="center">
        <v-col>
            <v-dialog
            v-model="dialog"
            persistent
            max-width="600px"
            >

                <v-card>
                    <v-card-title>
                        <span class="text-h5">Add Event</span>
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="10">
                                <v-select
                                v-model="eventType"
                                item-text="name"
                                item-value="bgColor"
                                :items="privateCalendars"
                                label="View Type"
                                outlined
                                
                                ></v-select>
                            </v-col>
                            <v-col>
                                <v-btn
                                class="ma-2 pa-0 align-center"
                                outlined
                                fab
                                color="indigo"
                                @click="openAddType()"
                                >
                                <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-card-text>
                    <v-card-text>
                        <v-text-field placeholder="Subject"></v-text-field>
                    </v-card-text>
                    <v-card-text>
                        <v-text-field placeholder="Location"></v-text-field>
                    </v-card-text>



                    <v-card-text>
                        <v-menu
                            v-model="startPicker"
                            :close-on-content-click="closeByclick"
                            :nudge-right="40"
                            transition="scale-transition"
                            offset-y
                            min-width="auto"
                        >
                            <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                    v-model="startDate"
                                    label="시작 날짜"
                                    prepend-icon="mdi-calendar"
                                    readonly
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="closeByclick = false"
                                ></v-text-field>
                            </template>
                            <v-date-picker
                            v-model="startDate"
                            @input="pickerOff(startPicker)"
                            ></v-date-picker>
                        </v-menu>
                    </v-card-text>
                    <v-card-text>
                        <v-menu
                            v-model="endPicker"
                            :close-on-content-click="closeByclick"
                            :nudge-right="40"
                            transition="scale-transition"
                            offset-y
                            min-width="auto"
                        >
                            <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                    v-model="endDate"
                                    label="종료 날짜"
                                    prepend-icon="mdi-calendar"
                                    readonly
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="closeByclick = false"
                                ></v-text-field>
                            </template>
                            <v-date-picker
                            v-model="endDate"
                            @input="pickerOff(endPicker)"
                            ></v-date-picker>
                        </v-menu>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="dialog = false"
                        >
                            Close
                        </v-btn>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="dialog = false"
                        >
                            Save
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
    
    <!-- Add Private Event Type Modal -->
    <v-row justify="center">
        <v-col>
            <v-dialog
            v-model="newType"
            persistent
            max-width="600px"
            >
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Add Type</span>
                    </v-card-title>

                    <v-card-text>
                        <v-text-field placeholder="Name"></v-text-field>
                    </v-card-text>
                    <v-card-text>
                        <v-text-field placeholder="Color"></v-text-field>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="newType = false"
                        >
                            Close
                        </v-btn>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="newType = false"
                        >
                            Save
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
</v-container>
</template>
<script>
import 'tui-calendar/dist/tui-calendar.css'
//import Calendar from '@toast-ui/vue-calendar/src/Calendar.vue'
import { Calendar } from '@toast-ui/vue-calendar';

// If you use the default popups, use this.
import 'tui-date-picker/dist/tui-date-picker.css';
import 'tui-time-picker/dist/tui-time-picker.css';
import themeConfig from './myTheme.js'

import axios from "axios";
import setToken from "../../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/wrapper/";

export default {
    data : () => {

        
      return {
            // calendar configurations
            themeConfig : themeConfig,
            events : [],
            calendarList: [
                {
                    id: '0',
                    name: 'Private',
                    group : 'private',
                    bgColor: '#ffffff',
                    borderColor: '#ffffff'
                },
                {
                    id: '1',
                    name: 'Company',
                    group : 'public',
                    bgColor: '#00a9ff',
                    borderColor: '#00a9ff'
                }
            ],

            //privateCalendars : [],

            scheduleList: [],

            selectedView: {
                    text : 'Monthly',
                    value : 'month'
            },
            viewModeOptions: [
                {
                    text : 'Monthly',
                    value : 'month'
                },
                {
                    text : 'Weekly',
                    value : 'week'
                },
                                {
                    text : 'Daily',
                    value : 'day'
                }
            ],

            // event modal
            dialog: false, // control modal on/off
            startPicker: false, // control modal on/off of start date's date-picker 
            endPicker: false, // control modal on/off of end date's date-picker 
            startDate: "", // start date for new private schedule
            endDate: "", // start date for new private schedule
            closeByclick : false, // controller to maintain date picker  
            
            eventType : {},
            newType : false,
            }  
    },

    methods : {
        setDate : function(){
            return (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
        },

        parseEvent : function(event){

            return {
                    id: event.id,
                    calendarId: event.group,
                    title: event.title,
                    category: 'allday',
                    dueDateClass: '',
                    start: Date.parse(event.start),
                    end: Date.parse(event.end)
                }

        },

        to : function(direction) {  
            this.$refs.tuiCalendar.invoke(direction); // tui calendar의 method를 call하기 위한 방법임. 
        },
        // http://forward.nhnent.com/hands-on-labs/toastui.calendar-timetable/05%20events.html#id2

        pickerOff : function(controller){
            console.log('modal off')
            controller = false  
            this.closeByclick = true
            
        },

        openAddType : function(){
            this.newType = true
        },

        AddType : function(){
            // private user event를 저장 
            // axios로 추가하고
            // calendar list에 추가하면
            // computed로 privateCalendars에 추가됨
        },
        
        onAfterRenderSchedule(e) {
            // 캘린더 전체를 렌더링한 이후 매 싱글 스케쥴에 적용됨
            let schedule = e.schedule;
            // use the element
            console.log(schedule);
        },
        onBeforeCreateSchedule(e) {
            // calendar cell 클릭하면 발생
            console.log('before Create')
            this.dialog = true
            // let the creation guide invisible
            let guide = e.guide;
            guide.clearGuideElement();
            
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
            // 아니면 그냥 정보만 보여주기
            console.log('schedule click')
            
        },
        onClickTimezonesCollapseBtn(e) {
            // tz collapse 버튼을 눌렀을 때
            console.log('tz collapse') 

        }

        },


    components: {
        Calendar
    },

    mounted() {
        this.startDate = this.setDate()
        this.endDate = this.setDate()

        axios({
            method : "GET",
            url : url,
            headers : setToken(),
            params : {
                content_type : "event",
                view_type : "calendar"
            }
        })
        .then(response => {
            let events = response.data
            let parsed = []       
            for (let i in events){
                parsed.push(this.parseEvent(events[i]))
            }
            this.scheduleList = parsed
        })
        .catch(response => {
            console.log("Failed", response);
        });

    },

    computed: {
        privateCalendars : function(){
            let arr = Array()
            let _calendarList = this.calendarList
            for (let i in _calendarList){
                if (_calendarList[i].group === 'private'){
                    arr.push(_calendarList[i])
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