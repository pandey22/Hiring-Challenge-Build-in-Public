<template>
    <div class="flex flex-col items-center bg-gray-100 min-h-screen p-6">
      <h1 class="text-3xl font-bold text-blue-700 mb-6">Teacher Dashboard</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
        <!-- Add Game Card -->
        <div class="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer hover:shadow-xl transition">
          <div class="text-5xl text-green-500 mb-4">➕</div>
          <h2 class="text-xl font-semibold">Add Game</h2>
        </div>
        
        <!-- Delete Game Card -->
        <div class="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer hover:shadow-xl transition">
          <div class="text-5xl text-red-500 mb-4">🗑️</div>
          <h2 class="text-xl font-semibold">Delete Game</h2>
        </div>
        
        <!-- Check Report Card -->
        <div class="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer hover:shadow-xl transition">
          <div class="text-5xl text-blue-500 mb-4">📊</div>
          <h2 class="text-xl font-semibold">Check Report</h2>
        </div>
      </div>
    </div>
  </template>