const fs = require("fs")

// Reads env vars
require("dotenv").config({ path: "src/.env" })

const puppeteer = require("puppeteer")

/**
 * Gets the current account and topic for production and returns the target urls
 * @param {string} path_account_file Path to accounts.json
 * @param {string} account_id Account identifier for accounts.json
 * @param {string} videoType Video type identifiert for accounts.json
 */
const getVideoTargets = (path_account_file, account_id, videoType) => {
	const rawData = fs.readFileSync(path_account_file)
	const parsedData = JSON.parse(rawData)
	// console.log(parsedData);

	const videoTargets =
		parsedData[`${account_id}`]["video_types"][`${videoType}`][
			"target_urls"
		]
	console.log(videoTargets)

	return videoTargets
}

// Deletes the previous files
try {
	fs.unlinkSync("data/temp/urls/bgurls.json")
	fs.unlinkSync("data/temp/urls/urls.json")
	fs.unlinkSync("data/temp/urls/urls0.json")
	//file removed
} catch (err) {
	//console.error(err)
}

// Gets the target links
const targets = getVideoTargets(
	"data/accounts/accounts.json",
	process.env.ACCOUNT_ID,
	process.env.VIDEO_TYPE
)

// Defines video parameters
let videoCount = 1
let videoLength = 15 // est. duration of the final vid in mins
let videoLengthPerTarget = Math.ceil(videoLength / targets.length) // Math.floor to save compute time and transform to int
// let urls_per_video = 0 // why?

/**
 * Main function that handles the process of retrieving TikTok urls
 * @param {string} target Url of target page on TikTok
 */
const getLinks = (target) => {
	// Launches the puppeteer instance
	puppeteer
		.launch({
			product: "firefox",
			headless: false,
			ignoreHTTPSErrors: true,
			args: ["-wait-for-browser"],
		})
		.then(async (browser) => {
			let urls = []
			let video_urls = []
			let background_urls = []

			// Puppeteer usage as normal
			let targetPath = await target
			console.log("Fetching links..")
			const page = await browser.newPage()
			await page.goto(targetPath, { waitUntil: "domcontentloaded" })

			await page.waitFor(7500)

			const cookies = await page.cookies()

			await autoScroll(page)

			/**
			 * Gets the video urls from the first page (trend/tag/influencer page)
			 */
			urls = await page.evaluate(() => {
				const results = []
				const items = document.querySelectorAll(
					".video-feed-item-wrapper"
				) // '.video-player')
				items.forEach((item) => {
					results.push({
						url: item.getAttribute("href"),
						text: item.innerText,
					})
				})
				return results
			})

			// Calulates the amount of videos to fetch
			let video_length_target_s = videoLengthPerTarget * 60 // videoLenghtPerTarget is in mins
			let avg_video_length = 15 // seconds
			urls_per_video = Math.round(
				video_length_target_s / avg_video_length
			)
			let urls_to_fetch = videoCount * urls_per_video

			// Randomize the list
			// (Helps to reduce duplicate content in consecutive videos)
			urls = shuffle(urls)

			// Fetches the video source and background urls
			// (Url is automatically shortened here)
			for (let i = 0, length = urls_to_fetch; i < length; i++) {
				link_count = i + 1
				console.log(
					"Fetching link " +
						"[" +
						link_count +
						"/" +
						urls_to_fetch +
						"]"
				)
				try {
					await page.goto(urls[i].url, {
						waitUntil: "domcontentloaded",
					}) // { waitUntil: 'networkidle2' } { waitUntil: 'networkidle0' }
					await page.waitFor(1500)

					// Get video src url
					const domElem = await page.evaluateHandle(() => {
						return document
							.querySelector("video")
							.getAttribute("src")
					})
					const video_url = domElem._remoteObject.value

					// Get video background url
					let background_url = await page.evaluate(() => {
						bi = document
							.querySelector(".image-card")
							.style.backgroundImage.slice(4, -1)
							.replace(/"/g, "")

						return bi
					})

					video_urls.push({
						url: video_url,
						bgurl: background_url,
						ref: urls[i].url,
						cookie: cookies,
					})
				} catch (e) {
					// console.log(e)
				}
			}

			// // Fetches the background image source urls
			// // Probably more time to let the site load
			// for (let i = 0, length = urls_to_fetch; i < length; i++) {
			//   console.log(`Fetching bg-img link [${i + 1}/${length}]`);
			//   try {
			//     await page.goto(urls[i].url, { waitUntil: "domcontentloaded" }); // { waitUntil: 'networkidle0'}
			//     await page.waitFor(2000);
			//     let background_url = await page.evaluate(() => {
			//       bi = document
			//         .querySelector(".image-card")
			//         .style.backgroundImage.slice(4, -1)
			//         .replace(/"/g, "");

			//       return bi;
			//     });

			//     background_urls.push({
			//       url: background_url,
			//       ref: urls[i].url,
			//     });
			//     console.log(`BG_URL: ${background_urls}`);
			//   } catch (e) {
			//     console.log(e);
			//   }
			// }
			// console.log(background_urls);

			// Stores all urls in json files
			const urlString = JSON.stringify(urls)
			let jsonString = JSON.stringify(video_urls)

			// const bgString = JSON.stringify(background_urls);

			// console.log(urlString);

			fs.appendFile("data/temp/urls/urls.json", urlString, (err) => {
				if (err) {
					console.log("Error writing file", err)
				} else {
					console.log("Successfully wrote file")
				}
			})

			// fs.appendFile("data/temp/urls/bgurls.json", bgString, (err) => {
			//   if (err) {
			//     console.log("Error writing file", err);
			//   } else {
			//     console.log("Successfully wrote file");
			//   }
			// });

			fs.appendFile(
				`data/temp/urls/download_urls.json`,
				jsonString,
				(err) => {
					if (err) {
						console.log("Error writing file", err)
					} else {
						console.log("Successfully wrote file")
					}
				}
			)

			await browser.close()
		})
}

/**
 * Automatically scrolls the infinite loop
 * @param {object} page Instance of a puppeteer page
 */
const autoScroll = (page) =>
	page.evaluate(
		async () =>
			await new Promise((resolve, reject) => {
				let totalHeight = 0
				const distance = 50 // Can be scrollheight
				// A higher scrollingTime equates to more links for the system to choose from
				const scrollingTime = 30000 // 20000 before
				const scrollingSpeed = 15
				const scrollCount = scrollingTime / scrollingSpeed

				let counter = 0

				const timer = setInterval(() => {
					// const scrollHeight = document.body.scrollHeight
					window.scrollBy(0, distance)
					totalHeight += distance

					if (counter >= scrollCount) {
						clearInterval(timer)
						resolve()
					}
					counter += 1
				}, scrollingSpeed)
			})
	)

/**
 * Shuffles an array
 * @param {array} array The array to be shuffled
 */
const shuffle = (array) => {
	var currentIndex = array.length,
		temporaryValue,
		randomIndex

	// While there remain elements to shuffle...
	while (0 !== currentIndex) {
		// Pick a remaining element...
		randomIndex = Math.floor(Math.random() * currentIndex)
		currentIndex -= 1

		// And swap it with the current element.
		temporaryValue = array[currentIndex]
		array[currentIndex] = array[randomIndex]
		array[randomIndex] = temporaryValue
	}

	return array
}

// Main execution loop
// Starts as many instances as needed - works way faster
// I don´t know how well other systems handle many instance

for (let idx = 0, length = targets.length; idx < length; idx++) {
	// console.log(idx)
	getLinks(targets[idx])
}
