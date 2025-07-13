


const fs = require('fs');

function countUniqueCharactersInFile(filePath) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error(`Error reading file: ${err.message}`);
      return;
    }

    const uniqueChars = new Set();
    for (const char of data) {
      uniqueChars.add(char);
    }

    console.log(`The file "${filePath}" contains ${uniqueChars.size} unique characters.`);
    console.log('Unique characters:', Array.from(uniqueChars).join(''));
  });
}


  const filename = "maps/Map18.map"
  
  countUniqueCharactersInFile(filename);


  terrain_costs = {
    '.': 1.0,   # Flat ground
    'B': float('inf'),
    'C': 3.0,
    'D': 4.0,
    'E': 2.0,
    'F': 3.5,
    'G': 1.5,
    'H': 2.5,
    'I': 2.0,
    'J': 4.5,
    'K': 5.0,
    'L': 10.0,
    'M': 6.0,
    'N': 1.0,
    'O': 1.0,
    '@': float('inf'),
    'T': float('inf')
}
