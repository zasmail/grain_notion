# Project Plan

> **Changelog (latest update):**  
> - Completed Step 7: Add endpoint for transcript assembly.  
> - Incorporated answers to open questions regarding test framework, data storage, secrecy, concurrency, and the URL replacement logic.  
> - Added "Plan" section to outline how we'll address these points in our implementation approach.
> - Added a new "Step-by-Step Implementation Plan" section to provide a more detailed project roadmap, while preserving the existing high-level "Plan" section.

*Important: Any time a change is made to the project, please update the changelog.*

## Overview
We are creating a Python-based Vercel cloud function to process a Grain video URL and return a structured transcript.  
• We currently have a local environment on http://localhost:3000 with a "Hello World" route.  
• We will continue to build locally until the plan is fully approved.

---

## Objectives

1. **URL Validation and Transformation**  
   - Validate that the URL matches the expected Grain format, e.g.,  
     https://grain.com/share/recording/<recordingId>/<sessionId>?tab=summary  
   - Force the URL to use "?tab=transcript" before fetching (replace any existing query param).  
   - Return a 400 error for incorrect or malformed URLs.  

2. **Fetch and Extract Data**  
   - Perform an HTTP GET to retrieve the Grain page.  
   - Use parsing (e.g., requests + BeautifulSoup) to locate the meta tag with name="grain:recording:json".  
   - Parse the embedded JSON data.  
   - Handle network errors (503) and malformed/missing JSON gracefully.  

3. **Process Speaker Data**  
   - Extract speaker info from `json.transcript.data.speakers`.  
   - Map speakerIds to speaker names.  
   - If info is missing, label as "Unknown Speaker" but keep distinct segments for each unknown speaker.  

4. **Process Transcript**  
   - Combine `json.transcript.data.speakerRanges` with `json.transcript.data.results`.  
   - Match each speaker range to its corresponding words.  
   - Join words with spaces, respecting existing punctuation.  
   - Ensure readable text output by removing duplicate spaces, etc.  

5. **Create Structured Output**  
   - Return an array of line objects with fields like:
     {
       "speaker": "John Doe",
       "speakerId": "<UUID>",
       "startIndex": 0,
       "endIndex": 10,
       "startMs": 0,
       "endMs": 5000,
       "transcript": "Welcome to our meeting about project planning.",
       "transcriptIndex": 0
     }
   - Maintain chronological order and increment `transcriptIndex` for each segment.  
   - Include a `metadata` object with:
     {
       "processingTime": "123ms",
       "wordCount": 1500, // ignoring punctuation
       "speakerCount": 5,
       "duration": "25m 30s"
     }

---

## Error Handling

1. **Invalid URL (HTTP 400)**  
   - Return a clear error message: "Invalid URL format for Grain recording."  

2. **Network Fails (HTTP 503)**  
   - Suggest retry, log error details for debugging.  

3. **Missing Transcript**  
   - Return partial data if possible, with a warning about the missing parts.  

4. **Unknown Speakers**  
   - Tag them as "Unknown Speaker," no merging of separate "Unknown Speaker" segments.  

5. **General Errors**  
   - Log the details (error message, stack) and return suitable HTTP codes.  
   - Provide a helpful error message in JSON (e.g., "errors" array).  

---

## Testing Considerations

1. **Test Data**  
   - Use known Grain URLs as primary test input.  
   - Compare generated transcript with an example expected output (docs/transcript_valid_response.json).  

2. **Output Format**  
   - Confirm the JSON matches the specified schema.  
   - Validate joining of words and punctuation.  

3. **Error Handling**  
   - Test malformed URLs, simulate network timeouts, remove meta tags to ensure 503 and partial data are handled.  

4. **Edge Cases**  
   - Empty transcripts.  
   - Single-speaker content.  
   - Overlapping or out-of-order segments.  

5. **Performance**  
   - Typical meetings are under one hour; keep an eye on performance for large transcripts.  

---

## Resources

- Example URL:  
  https://grain.com/share/recording/5241a92e-1ab8-47c8-8f54-ec9f3649eac5/5lcMmg64fZU5DziAUDsBuEANYo968z0e1rBiSHVi?tab=summary  
- Sample output for testing:  
  docs/transcript_valid_response.json  

---

## Risks

- Changes to Grain's HTML or meta data format could break scraping.  
- Long transcripts might raise performance or memory concerns.  
- Missing speaker data could complicate transcript parsing.  

---

## Additional Notes

- Currently developing locally at http://localhost:3000; local route confirmed working.  
- Word counts ignore punctuation.  
- Strict TDD will be followed.  
- Keep the changelog updated with each change.  

---

## Plan

Below is the high-level approach based on the clarifications provided:

1. **Test Framework**  
   - We will use a Python testing framework such as pytest for simplicity and readability, given that it's widely adopted and developer-friendly.  

2. **Data Storage**  
   - We do not need to store the original transcript. Once the transcript is flattened, we can simply return the processed JSON.  

3. **Secrecy & Environment**  
   - We will store any sensitive credentials or API keys (if needed) in environment variables.  
   - Since there is no immediate need for secrets beyond the default fetch, we will keep Vercel configuration minimal for now.  

4. **Concurrent Requests**  
   - We will rely on the default scaling behavior of Vercel's serverless platform to handle concurrent requests. If needed, we'll add caching layers or concurrency limits in future phases.  

5. **Final URL Logic**  
   - We will accept any incoming queries but replace them with "?tab=transcript" before fetching the page to ensure we always get the transcript view.  

6. **Future Additional Functionality**  
   - Any potential enhancements (e.g., more advanced speaker diarization or analytics) will be considered in future sprints. For now, we focus on a working transcript solution.  

> **Important**: Continue updating this plan and the changelog whenever new decisions or changes are made.

---

## Step-by-Step Implementation Plan

Below is a more detailed, step-by-step plan to guide development:

1. **Repository Setup & Development Environment**  
   - Confirm local Python environment and install necessary dependencies (requests, BeautifulSoup, pytest, etc.).
   - Use `vercel dev` to run the local server and ensure it is ready to accept new routes or endpoints.
   - **Status**: Completed

2. **Implement TDD for URL Validation**  
   - Write tests to ensure the URL format is correct (valid vs. invalid URLs).  
   - Implement the function that normalizes or replaces the query parameter with "?tab=transcript."  
   - Return HTTP 400 if the URL fails validation tests.
   - Create a new route for the URL validation function in the api folder.
   - **Status**: Completed

3. **HTTP Fetch & HTML Parsing**  
   - Write tests expecting a successful HTML fetch and valid meta tag extraction.  
   - Implement the fetch logic (via requests or similar library) and handle potential network errors.  
   - Parse the fetched HTML with BeautifulSoup, locating the meta tag with "grain:recording:json" content.
   - **Status**: Completed

4. **JSON Parsing & Error Handling**  
   - Write tests that simulate missing or malformed JSON.  
   - Rely on the data from "(meta_tag.json)" to test the JSON parsing.
   - Implement JSON parsing, logging any errors, and returning HTTP 503 if the transcript is inaccessible.  
   - Return partial data if only some sections are malformed (if feasible).
   - **Status**: Completed

5. **Speaker Data Extraction**  
   - Write tests for "Unknown Speaker" scenarios.  
   - Implement mapping of speakerIds to speaker names, ensuring unknown speakers are labeled distinctly.
   - **Status**: Completed

6. **Transcript Assembly**  
   - Write tests covering proper word spacing, punctuation handling, and concatenation.  
   - Merge speaker ranges (timing) with the actual word data.  
   - Return clean text for each segment, removing extra spaces.
   - **Status**: Completed

7. **Add endpoint for transcript assembly**  
   - Create a new route in the api folder for the transcript assembly function.
   - Rely on the data from "(meta_transcript_output.json)" to test the transcript assembly, this should match the output from "https://grain.com/share/recording/5241a92e-1ab8-47c8-8f54-ec9f3649eac5/5lcMmg64fZU5DziAUDsBuEANYo968z0e1rBiSHVi?tab=summary"
   - Add tests for the endpoint in the tests folder.
   - **Status**: Completed

8. **Collect Metadata**  
   - Functionality to the transcript endpoint to collect chapters, outcomes, and action items.
     - Chapters can be found under "intelligence" > "chapters" > "data". Keep the format unchanged from the original data.
     - Outcomes can be found under "intelligence" > "summaryTabSections" where the "section" > "title" is "Outcomes". Return the "data" array under "outcomes".
     - Action items can be found under "intelligence" > "summaryTabSections" where the "section" > "title" is "Action Items". Return the "data" array under "action_items".
   - Rely on the data from "(meta_tag.json)" to test the metadata collection.
   - **Status**: Outstanding

9. **Structured Output Assembly**  
   - Write tests checking that each segment's JSON format matches the schema.  
   - Implement the functionality to generate line objects with incrementing transcriptIndex.  
   - Compute metadata (processing time, wordCount ignoring punctuation, speakerCount, duration).
   - **Status**: Outstanding

10. **Integrate Error Handling & Logging**  
    - Ensure that each error path (invalid URL, network fail, missing transcript) returns a suitable HTTP code and a JSON body with error details.  
    - Log errors for debugging while still returning stable, partial responses if possible.
    - **Status**: Outstanding

11. **Refinement & Additional Testing**  
    - Expand tests to include edge cases (empty transcript, single speaker, overlapping ranges).  
    - Verify performance for typical meeting lengths (~1 hour of audio/video).  
    - Conduct code reviews to ensure TDD best practices are followed.
    - **Status**: Outstanding

12. **Deployment & Post-Deployment Checks**  
    - Deploy to Vercel once the core functionality and tests pass consistently.  
    - Verify that the serverless environment resolves dependencies correctly.  
    - Conduct final checks with real Grain URLs to confirm everything is working as expected.
    - **Status**: Outstanding

> **Next Steps**: Continue to update this "Step-by-Step Implementation Plan" as new insights arise or as we adjust tasks in response to testing feedback.

