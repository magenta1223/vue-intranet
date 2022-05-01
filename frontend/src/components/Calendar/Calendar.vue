<template>
<v-container>
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

    <v-row>
        <v-col cols="12">
    
            <Calendar
            ref="tuiCalendar"
            :view="selectedView.value"
            :calendars="calendarList"
            :schedules="scheduleList"
            :theme="themeConfig"
            
            :scheduleView="scheduleView"
            :month="month"
            :week="week"
            />
            <v-btn
            class="mx-2"
            fab
            color="indigo"
            :click="eventCreateModal()"
            >
                <v-icon>
                    mdi-plus
                </v-icon>
            </v-btn>
        </v-col>
    </v-row>
    <v-row justify="center">
        <v-dialog
        v-model="dialog"
        persistent
        max-width="600px"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                color="primary"
                dark
                v-bind="attrs"
                v-on="on"
                >
                Open Dialog
                </v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="text-h5">Add Event</span>
                </v-card-title>
                <v-card-text>
                    <v-select
                    item-text="text"
                    itme-value="value"
                    :items="viewModeOptions"
                    v-model="selectedView.value"
                    label="View Type"
                    outlined
                    ></v-select>
                </v-card-text>
                <v-card-text>
                    <v-text-field placeholder="Subject"></v-text-field>
                </v-card-text>
                <v-card-text>
                    <v-text-field placeholder="Location"></v-text-field>
                </v-card-text>

                <v-card-text>
                    <v-menu
                        v-model="menu1"
                        :close-on-content-click="true"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                                v-model="startdate"
                                label="시작 날짜"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                        v-model="startdate"
                        @input="menu1 = false"
                        ></v-date-picker>
                    </v-menu>
                </v-card-text>
                <v-card-text>
                    <v-menu
                        v-model="menu2"
                        :close-on-content-click="true"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                                v-model="enddate"
                                label="종료 날짜"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                        v-model="enddate"
                        @input="menu2 = false"
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
    </v-row>

</v-container>
</template>
<script>
import 'tui-calendar/dist/tui-calendar.css'
import Calendar from '@toast-ui/vue-calendar/src/Calendar.vue'

// If you use the default popups, use this.
import 'tui-date-picker/dist/tui-date-picker.css';
import 'tui-time-picker/dist/tui-time-picker.css';
import themeConfig from './myTheme.js'

import axios from "axios";
import setToken from "../../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/wrapper/";

export default {
    data : () => {

        console.log(themeConfig)
      return {
            // calendar configurations
            themeConfig : themeConfig,
            events : [],
            readonly : true,            
            calendarList: [
                {
                    id: '0',
                    name: 'Private',
                    bgColor: '#ffffff',
                    borderColor: '#ffffff'
                },
                {
                    id: '1',
                    name: 'Company',
                    bgColor: '#00a9ff',
                    borderColor: '#00a9ff'
                }
            ],

            scheduleList: [],
            scheduleView:true,
            month: {
                startDayOfWeek: 0
            },
            week: {
                showTimezoneCollapseButton: true,
                timezonesCollapsed: true
            },
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
            dateRange: '',

            // add event modal
            dialog: false,
            menu1: false,
            menu2: false,
            modal: false,
            startdate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
            enddate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
}  
    },

    methods : {
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
        
        eventCreateModal : function(){
            //팝업을 띄우고

            // 
        }

        },


    components: {
        Calendar
    },

    mounted() {

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