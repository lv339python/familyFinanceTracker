<template>
  <div id="calendar">
    <v-calendar :attributes='attrs'></v-calendar>
  </div>
</template>

<script>

export default {

  data() {
    return {
      // Attributes are supplied as an array
      attrs: [
        // This is a single attribute
        {
          // An optional key can be used for retrieving this attribute later,
          // and will most likely be derived from your data object
          key: 1,
          // The attribute can contain any of the following object types
          highlight: {
            backgroundColor: '#ff8080',     // Red background
            borderColor: '#ff6666',
            borderWidth: '2px',
            borderStyle: 'solid',
          },
          dot: {
            backgroundColor: '#ac1300', // Turquoise dot
          },
          bar: {
            backgroundColor: '#794dff',     // Purple bar
          },
          popover: {
            label: "you just popovered this date"
          },
          // Supply your custom data object for later access, if needed
          customData: {},
          // We also need some dates to know where to display the attribute
          // We use a single date here, but it could also be a date range
          //  or a complex date pattern.
          // Arrays are also allowed
          dates: new Date(2018, 8, 28),
          // You can optionally provide dates to exclude.
          // All other dates are used by the attributed.
          excludeDates: null,
          // Think of `order` like `z-index`
          // If order > 0, this attribute will overlap all the other attributes
          order: 0
        },

      ],
    }
  },
};

</script>
<style>
#calendar{
  position:absolute;
  bottom:0;
}
</style>
