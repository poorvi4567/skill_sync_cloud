async function loadSkills() {
    const res = await fetch("http://127.0.0.1:8000/skills");
    const skills = await res.json();

    const dropdown = document.getElementById("skillDropdown");
    dropdown.innerHTML = "";

    skills.forEach(skill => {
        const option = document.createElement("option");
        option.value = skill.name;
        option.textContent = skill.name;
        dropdown.appendChild(option);
    });
}

loadSkills();

async function submitLearningInterest() {
    const username = localStorage.getItem("username");
    const skillName = document.getElementById("skillDropdown").value;

    const res = await fetch("http://127.0.0.1:8000/user-skills/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username,
            skill_names: [skillName]
        })
    });

    const data = await res.json();
    alert("Skill added successfully!");
    loadUserSkills();
}

async function loadUserSkills() {
    const username = localStorage.getItem("username");

    const res = await fetch(`http://127.0.0.1:8000/user-skills/${username}`);
    const skills = await res.json();

    const list = document.getElementById("userSkillList");
    list.innerHTML = "";

    skills.forEach(s => {
        const li = document.createElement("li");
        li.className = "list-item";
        li.textContent = s.skill_name;
        list.appendChild(li);
    });
}

loadUserSkills();

