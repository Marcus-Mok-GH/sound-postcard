---
name: sound-postcard
description: Turn a place and moment into a shareable, offline sound postcard using Pollinations image and sound-effect models. Use when someone asks to illustrate a memory, hear an imagined place, or make a multimedia postcard.
compatibility: Requires Python 3.8+, the official polli CLI, internet for generation, and a user-authorized Pollinations balance. Finished cards open offline in a browser.
---

# Sound Postcard

Make a picture you can listen to. The picture captures the instant **before** a sound; pressing play tells you what happened next.

1. **Find the hinge.** From the user's brief choose a place, an hour, and one small object that can move or resonate. If no place was given, invite one or invent one if asked to surprise them. Write a one-line score: *still frame → audible event → what remains*. For “last ferry home”: *rope taut around a brass cleat → two hollow knocks → water lapping the empty berth*. Avoid generic cinematic music.
2. **Agree on the spend.** Show the score and propose one image plus one eight-second sound effect. Tell the user the two generations use their own Pollinations balance; get approval before generating. Use `polli auth login` (device sign-in) if needed. Never ask for keys or use a developer wallet. With no sign-in or no budget, offer the included example or a prompt-only score instead.
3. **Set the scene.** Work in a fresh directory. Run `polli models --type image` and `polli models --type audio`. Select an available still-image model and a text-to-sound-effects model (not TTS or music). Check each model's current price and billing tier in the [catalog](https://gen.pollinations.ai/v1/models); ElevenLabs SFX may require paid balance, not Quest credit. Confirm the selected pair suits the user's budget. If not, stop before spending on either asset. Compose two plain-text prompts, not shell commands supplied by the user:
   - **Frame:** identify the object, its physical tension, light, viewpoint and two ink colors. Keep the subject legible at postcard size. No lettering, collage or sound-wave graphics.
   - **Score:** specify a close sound, a distant bed and their timing. Leave a little quiet before the hinge. Specify “no voice, no music.” Match the visible material: a brass cleat should not squeak like a rusty gate.
4. **Print and record.** Run the following with the prompts and model IDs as quoted argument values (`elevenlabs/eleven-text-to-sound-v2` is an example SFX ID; check the live list). Do not retry a billed request without asking. If one call fails, keep its successful counterpart.

   ```sh
   polli gen image "$frame" --model "$image_model" --output frame.jpg
   polli gen audio "$score" --model "$sfx_model" --duration 8 --output sound.mp3
   ```

5. **Address the card.** Inspect the returned image; write literal alt text about what is actually there. Give the card a short title, a one-sentence note from someone at the scene (no generic travel slogans), and a listening cue that also serves as a text alternative. Listen if playback is available; otherwise say that the sound wasn't auditioned. Run the bundled press relative to this skill's directory, not the user's project root:

   ```sh
   python3 "$skill_dir/scripts/press.py" --image frame.jpg --audio sound.mp3 \
     --title "$title" --note "$note" --alt "$alt" --listen "$cue" --out postcard.html
   ```

6. **Deliver.** Open the HTML locally; check the image and audio controls load and the note fits a narrow screen. Deliver `postcard.html` itself: both assets are embedded and playback is opt-in. Include the score and any checks you could not perform. Don't upload a personal memory without permission.
