const nameList = [
  "Time",
  "Past",
  "Future",
  "Dev",
  "Fly",
  "Flying",
  "Soar",
  "Soaring",
  "Power",
  "Falling",
  "Fall",
  "Jump",
  "Cliff",
  "Mountain",
  "Rend",
  "Red",
  "Blue",
  "Green",
  "Yellow",
  "Gold",
  "Demon",
  "Demonic",
  "Panda",
  "Cat",
  "Kitty",
  "Kitten",
  "Zero",
  "Memory",
  "Trooper",
  "XX",
  "Bandit",
  "Fear",
  "Light",
  "Glow",
  "Tread",
  "Deep",
  "Deeper",
  "Deepest",
  "Mine",
  "Your",
  "Worst",
  "Enemy",
  "Hostile",
  "Force",
  "Video",
  "Game",
  "Donkey",
  "Mule",
  "Colt",
  "Cult",
  "Cultist",
  "Magnum",
  "Gun",
  "Assault",
  "Recon",
  "Trap",
  "Trapper",
];

class Platform {
  constructor(resources = [], levels = []) {
    this.resources = resources;
    this.levels = [];
    this.currentLevel = 0;
  }
  next() {
    const nextNum = this.currentLevel + 1;
    this.currentLevel =
      nextNum <= this.levels.length - 1 ? nextNum : this.levels.length - 1;
    console.log(this.resources);
    this.levels[this.currentLevel].people.forEach((person) => {
      const food = Math.floor(Math.random() * this.resources.length);
      if (person.makeDecision(this.resources[food])) {
        this.resources.splice(food, 1);
      }
      console.log(this.resources);
    });
    console.log(
      "Level:",
      this.currentLevel,
      "Resources count:",
      this.resources.length
    );
  }
}

class Resource {
  constructor(name, delicious) {
    this.name = name;
    this.delicious = delicious;
  }
}

class Level {
  constructor(lvl) {
    this.lvl = lvl;
    this.people = [];
  }
  addPerson(person) {
    this.people.push(person);
  }
  getPeople() {
    return [...this.people];
  }
}

class Person {
  constructor(name, percent) {
    this.name = name;
    this.percent = percent;
  }
  makeDecision(resource) {
    if (resource) {
      const finalPercent = Math.min(this.percent + resource.delicious * 5, 100);
      const random = Math.floor(Math.random() * 100) + 1;
      return finalPercent > random;
    }
  }
}
const resources = [
  {
    name: "apple",
    delicious: 1,
  },
  {
    name: "cake",
    delicious: 3,
  },
  {
    name: "water",
    delicious: 2,
  },
  {
    name: "cookie",
    delicious: 1,
  },
];
function generateResources(res) {
  const resources = [];
  res.forEach((resource) => {
    for (let i = 0; i < Math.floor(Math.random() * 5); i++)
      resources.push(new Resource(resource.name, resource.delicious));
  });
  return resources;
}
const platform = new Platform(generateResources(resources));

let levels = [];
for (let i = 0; i < 10; i++) {
  const person1 = new Person(
    nameList[Math.floor(Math.random() * nameList.length)],
    Math.floor(Math.random() * 100) + 1
  );
  const person2 = new Person(
    nameList[Math.floor(Math.random() * nameList.length)],
    Math.floor(Math.random() * 100) + 1
  );
  let level = new Level(i);
  level.addPerson(person1);
  level.addPerson(person2);

  platform.levels.push(level);
}

for (let i = 0; i < platform.levels.length; i++) {
  platform.next();
}
