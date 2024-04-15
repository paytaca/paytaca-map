<template>
    <div>
      <h2>Locations</h2>
      <ul>
        <li v-for="location in locations" :key="location.id">
          {{ location.name }} ({{ location.latitude }}, {{ location.longitude }})
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        locations: [],
      };
    },
    mounted() {
      axios.get('http://localhost:8000/api/merchants/')
        .then(response => {
          this.locations = response.data;
        })
        .catch(error => {
          console.error('Error fetching locations:', error);
        });
    },
  };
  </script>

  