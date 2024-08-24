/** @odoo-module **/

export const primaryBackgroundColors = [
    'rgb(255, 187, 92)',
    'rgb(255, 155, 80)',
    'rgb(226, 94, 62)',
    'rgb(198, 61, 47)',
]

export const auxiliarColor = [
    'rgb(0,255,255)',
];

export const auxiliarColorSecondary = [
    'rgb(20,167,72)',
];

export const secondaryBackgroundColors = [
    'rgb(242, 133, 133)',
    'rgb(255, 164, 71)',
    'rgb(255, 252, 155)',
    'rgb(255, 87, 127)',
    'rgb(255, 136, 75)',
    'rgb(255, 211, 132)',
    'rgb(255, 249, 176)',
    'rgb(255, 96, 0)',
    'rgb(255, 165, 89)',
    'rgb(255, 230, 199)',
];

// Function to get a random color from a list of colors, without repeating colors
export default function getRandomColor(listOfColors, dataLength) {
    let usedColors = [];
    for (let i = 0; i < dataLength; i++) {
        const availableColors = listOfColors.filter(color => !usedColors.includes(color));

        if (availableColors.length === 0) {
            // if all colors have been used, reset the used colors
            usedColors = [];
        }

        const randomColor = availableColors[Math.floor(Math.random() * availableColors.length)];
        usedColors.push(randomColor);
        return randomColor;
    }

}
