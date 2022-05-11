<template>
    <v-container>
        <v-row justify="center">
            <v-col>
                <v-dialog
                v-model="dialog"
                max-width="600px"
                persistent
                >

                    <v-card>
                        <v-card-title>
                            <span class="text-h5">{{action}} Event</span>
                        </v-card-title>
                        <v-card-text>
                            <v-row>
                                <v-col cols="10">
                                    <v-select
                                    v-model="eventGroup"
                                    item-text="name"
                                    item-value="id"
                                    :items="calendarGroups"
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
                            <v-text-field v-model="title" placeholder="Title"></v-text-field>
                        </v-card-text>
                        <v-card-text>
                            <v-textarea v-model="description" placeholder="Description"></v-textarea>
                        </v-card-text>

                        <v-card-text>
                            <datePicker v-model="startDate"/>
                        </v-card-text>
                        <v-card-text>
                            <datePicker v-model="endDate"/>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                color="blue darken-1"
                                text
                                @click="dialogOff()"
                            >
                                Close
                            </v-btn>
                            <v-btn
                                color="blue darken-1"
                                text
                                @click="saveEvents()"
                            >
                                Save
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-col>
        </v-row>
        <v-row justify="center">
        <v-col>
            <v-dialog
            v-model="newType"
            persistent
            max-width="300px"
            >
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Add Type</span>
                    </v-card-title>

                    <v-card-text>
                        <v-text-field v-model="typeName" placeholder="Name"></v-text-field>
                    </v-card-text>
                    <v-color-picker
                    v-model="typeColor"
                    class="ma-2"
                    show-swatches
                    swatches-max-height="500px"
                    ></v-color-picker>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="colorOff()"
                        >
                            Close
                        </v-btn>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="AddType()"
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
import axios from "axios";
import setToken from "../../js_utils/token.js"
import datePicker from "../BaseComponents/DatePicker.vue"

let url = "http://127.0.0.1:8000/api/wrapper/";

export default {
    data : () => {
        return {
            // controllers
            startPicker: false, // control modal on/off of start date's date-picker 
            endPicker: false, // control modal on/off of end date's date-picker 
            closeByclick : false, // controller to maintain date picker  
            newType : false,
            
            // fields
            eventGroup : "",
            title : "",
            description : "",
            startDate : "",
            endDate : "",
            typeName : "",
            typeColor : "",
            
        }

    },

    components :{
        datePicker
    },

    props : ['calendarGroups', 'dialog', 'default_date', 'schedule'],

    methods : {
        setDate : function(){
            return (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
        },

        dialogOff : function(){
            this.$emit('_dialog', false)
        },

        colorOff : function(){
            console.log(this.typeColor.substr(0,7))
            this.newType = false
        },




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
            axios({
                method : "POST",
                url : url,
                headers : setToken(),
                params : {
                    type : 'Event',
                    name : this.typeName,
                    color : this.typeColor.substr(0,7),
                    user_id : localStorage.getItem('user'),
                    is_private : true,
                    content_type : "eventgroup"
                }
            }).then(response => {
                console.log(response.data)

                this.$emit('newGroup', response.data)
                this.newType = false
            }).catch(response => {
                console.log('개같이 멸망')
            })
        },



        saveEvents : function() {
            
            if (this.action === "Update") {
                let index = this.schedule.raw.index
                axios({
                    method : "PUT",
                    url : url + this.schedule.raw.wrapper_id +'/',
                    headers : setToken(),
                    params : {
                        content_type : "event",
                        user_id : localStorage.getItem('user'),
                        event_group_id : this.eventGroup,
                        title : this.title,
                        description : this.description,
                        start: this.startDate, // start date for new private schedule
                        end: this.endDate,
                        is_private : true,
                        attendees : [],
                        
                    }
                }).then( (response) => {
                    console.log('성공')
                    console.log(index)
                    this.$emit('newEvent', { data : response.data, index : index  })


                }).catch( (response) => {
                    console.log(response)
                })

            } else {
                axios({
                    method : "POST",
                    url : url,
                    headers : setToken(),
                    params : {
                        content_type : "event",
                        user_id : localStorage.getItem('user'),
                        event_group_id : this.eventGroup,
                        title : this.title,
                        description : this.description,
                        start: this.startDate, // start date for new private schedule
                        end: this.endDate,
                        is_private : true,                        
                    }
                }).then( (response) => {
                    this.$emit('newEvent', { data : response.data, index : -1  })


                }).catch( (response) => {
                    console.log(response)
                })
            }
            
            this.dialogOff()
        }
    },

    mounted() {
        console.log(this.default_date)
        this.startDate = this.default_date
        this.endDate = this.default_date
    },

    watch : {
        default_date : function(){
            this.startDate = this.default_date
            this.endDate = this.default_date
        }
    },
    
    computed : {
        action : function() {
            console.log(this.schedule)
            if (this.schedule === ""){
                this.eventGroup = ""
                this.title = ""
                this.description = ""
                this.startDate = this.default_date
                this.endDate = this.default_date
                return "Add"
            } else {
                this.eventGroup = this.schedule.calendarId
                this.title = this.schedule.title
                this.description = this.schedule.body
                this.startDate = this.schedule.start._date.toISOString().substr(0, 10)
                this.endDate = this.schedule.end._date.toISOString().substr(0, 10)

                return "Update"
            }
        }
    }
    
}
</script>
