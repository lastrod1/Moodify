const URL = 'api/load-songs';

export async function getRecommendedSongs(moodIds, genreIds) {
    const moodQuery = moodIds.join(',');
    const genreQuery = genreIds.join(',');

    const url = `${URL}?moods=${moodQuery}&genres=${genreQuery}`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to load songs. Status: ${response.status}`);
    }
    const data = await response.json();
    return data.songs || [];
}