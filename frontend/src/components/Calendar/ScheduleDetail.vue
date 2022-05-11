<template>
    

    <v-dialog v-model="open" :overlay-opacity="0" max-width="300" elevation-12>
        <div :style="{'background-color':color, height:'10px'}">
        </div>
        <v-card>
            
                <v-card-title>
                    <span class="text-h5"> {{schedule.title}}</span> <!-- private이면? private icon 표시  -->
                    <v-icon v-if="schedule.isPrivate" small>fa-lock</v-icon> <!-- 마우스 오버 시 private event 표시 -->
                </v-card-title>
                <v-card-text v-if="!schedule.isPrivate">
                    Author : {{schedule.raw.author}}
                </v-card-text>
                <v-card-text v-if="!schedule.isPrivate">
                    Attendees : {{schedule.attendees}}
                </v-card-text>

                <v-card-text>
                    {{parseDate(schedule.start._date, 'YYYY-MM-DD')}} ~ {{parseDate(schedule.end._date, 'YYYY-MM-DD')}}
                </v-card-text>
                <v-card-text>
                    {{schedule.body}}
                </v-card-text>
                <v-card-text v-if="isPermmitted(schedule)">
                    <v-row>
                        <v-col cols="6" class="text-center">
                            <v-btn @click="editEvent()">
                                Edit
                            </v-btn>
                        </v-col>
                        <v-col cols="6" class="text-center">
                            <v-btn @click="deleteEvent()">
                                Delete
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card-text>
                <!-- 권한이 있으면 수정 / 삭제 버튼  -->

        </v-card>
    </v-dialog>



</template>

<script>
import parseDate from "../../js_utils/date.js"
import axios from "axios";
import setToken from "../../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/wrapper/";

export default {
    data : () => {
        return {
            x : 0,
            y : 0,
            open : false,
            prev_event : "",
            loading: false,
            selection: 1,

            color : '#ff00ff'
        }
    },

    props : ['event'],

    methods : {
        parseDate,
        fetch : function() {
            //this.$emit('reopen', undefined)
        },
        onClickOutside : function(){
            //this.open= false

        },
        editEvent : function(schedule){

            this.open = false
            console.log(this.schedule)
            this.$emit( 'updateEvent', this.schedule)

        },
        deleteEvent :  function(){

            axios({
                method : "DELETE",
                headers : setToken(),
                url : url + this.schedule.raw.wrapper_id + '/'
            }).then((response) => {
                console.log('delete')
            }).catch((response) => {
                console.log('Failed', response)
            })

            this.open = false
            this.$emit('deleteEvent', this.schedule.raw.index)
            
        },

        isPermmitted : function(schedule){
            
            if (localStorage.getItem('user') === String(schedule.raw.author)){
                return true
            } else {
                return false
            }

        },

        
      
    },

    watch :{

        event: {
                handler(newParam, oldParam){

                    this.x = newParam.event.pageX
                    this.y = newParam.event.pageY
                    this.open = true
                    this.prev_event = newParam
                    this.schedule = newParam.schedule

                    this.color = this.schedule.bgColor


                },
                deep : true,
                immediate: true
            },
    }
}
</script>


<style scoped>


</style>