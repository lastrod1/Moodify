export async function getGenreList() {
    const response = await fetch('/api/genres');
    const data = await response.json();
    console.log(data);

    return data.genres;
}