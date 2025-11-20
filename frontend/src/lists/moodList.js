export async function getMoodList() {
    const response = await fetch('/api/moods');
    const data = await response.json();
    console.log(data);

    return data.moods;
}