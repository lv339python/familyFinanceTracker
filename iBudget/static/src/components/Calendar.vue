<template>
    <div id="calendar">
        <b-btn id="popoverButton-sync" variant="info">Show Calendar</b-btn>
        <b-popover id="popover" :show.sync="show" target="popoverButton-sync" placement="bottom">
            <v-calendar :attributes='attrs'></v-calendar>
        </b-popover>
    </div>
</template>

<script>

    export default {
        name: 'Calendar',
        data() {
            return {
                // Attributes are supplied as an array
                show: false,
                attrs: [
                    // This is a single attribute
                    {
                        // An optional key can be used for retrieving this attribute later,
                        // and will most likely be derived from your data object
                        key: 2,
                        // The attribute can contain any of the following object types
                        bar: {
                            backgroundColor: '#794dff',     // Purple bar
                        },
                        popover: {
                            label: "you just captured another date"
                        },
                        // Supply your custom data object for later access, if needed
                        customData: {},
                        // We also need some dates to know where to display the attribute
                        // We use a single date here, but it could also be a date range
                        //  or a complex date pattern.
                        // Arrays are also allowed
                        dates: new Date(2018, 9, 7),
                        // You can optionally provide dates to exclude.
                        // All other dates are used by the attributed.
                        excludeDates: null,
                        // Think of `order` like `z-index`
                        // If order > 0, this attribute will overlap all the other attributes
                        order: 0
                    },
                    {
                        key: 2,

                        dot: {
                            backgroundColor: '#ac1300', // Turquoise dot
                        },

                        popover: {
                            label: "you just captured this date"
                        },

                        customData: {},

                        dates: new Date(2018, 9, 28),

                        excludeDates: null,

                        order: 0
                    },
                    {
                        key: 2,

                        dot: {
                            backgroundColor: '#ac1300', // Turquoise dot
                        },

                        popover: {
                            label: "you just captured this date"
                        },
                        customData: {},

                        dates: new Date(2018, 9, 23),

                        excludeDates: null,

                        order: 0
                    },
                    {

                        key: 2,

                        dot: {
                            backgroundColor: '#ac1300', // Turquoise dot
                        },

                        popover: {
                            label: "you just captured this date"
                        },

                        customData: {},

                        dates: new Date(2018, 9, 22),

                        excludeDates: null,

                        order: 0
                    },

                    {

                        key: 2,

                        highlight: {
                            backgroundColor: '#ff8080',     // Red background
                            borderColor: '#ff6666',
                            borderWidth: '2px',
                            borderStyle: 'solid',
                        },


                        popover: {
                            label: "This is the date range"
                        },

                        customData: {},

                        dates: {
                            start: new Date(2018, 9, 10),
                            end: new Date(2018, 9, 20)
                        },

                        excludeDates: null,

                        order: 0
                    },
                ],
            }
        },
    };

</script>
<style>
    #calendar {
        position: relative;
        /*bottom: 0;*/
        top: 0;
        margin-left: auto;

    }

    .c-pane-container {
        float: right;
    }

    .bs-popover-bottom {
        padding-bottom: 0.5rem;
    }
</style>
