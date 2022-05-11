<template>
    <v-menu
    v-model="picker"
    :close-on-content-click="closeByclick"
    :nudge-right="40"
    transition="scale-transition"
    offset-y
    min-width="auto"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-text-field
                v-model="value"
                label="생년월일"
                prepend-icon="mdi-calendar"
                v-bind="attrs"
                v-on="on"
                @click="closeByclick = false"
                @change="onChanged"
                :readonly="readonly"
            ></v-text-field>
        </template>
        <v-date-picker
        v-model="value"
        @input="pickerOff(picker)"
        :readonly="readonly"
        ></v-date-picker>
    </v-menu>    
</template>

<script>

export default {
    data() {
        return {
            closeByclick : false,
            picker : false
            }
    },
    props : ['value', 'readonly'],

    methods : {
        pickerOff : function(controller){
            console.log('modal off')
            controller = false  
            this.closeByclick = true
            this.onChanged()
        },

        onChanged : function(){
            console.log(this.readonly)
            this.$emit('input', this.value)
        }

    }

}
</script>


