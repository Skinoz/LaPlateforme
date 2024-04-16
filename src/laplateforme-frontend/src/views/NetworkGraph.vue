<script setup lang="ts">
import { defineConfigs } from 'v-network-graph'
import data from '../data/data'

const configs = defineConfigs({
  node: {
    selectable: true,
    scalingObjects: true
  }
})
</script>

<template>
  <div class="flex">
    <div class="graph-container">
      <v-network-graph
        class="graph"
        :nodes="data.nodes"
        :edges="data.edges"
        :layouts="data.layouts"
        :configs="configs"
      />
    </div>
    <div class="bg-[#072637]">
      <div class="bg-[#051A26] border-2 p-4">
        <h1 class="font-semibold text-white w-40">Vm List</h1>
      </div>
    </div>
  </div>
</template>

<style>
.graph-container {
  width: 100%;
  height: calc(100vh - 70px); /* 70px is the height of the navigation bar */
  display: flex;
  justify-content: center; /* Centrer horizontalement */
  align-items: center; /* Centrer verticalement */
}

.graph {
  width: 100%; /* Utilise toute la largeur de son parent */
  height: 100%; /* Utilise toute la hauteur de son parent */
  max-width: 100%; /* Ne dépasse pas la largeur de son parent */
  max-height: 100%; /* Ne dépasse pas la hauteur de son parent */
}
</style>
