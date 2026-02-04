package pokemonTextBased;

import javax.sound.sampled.*;
import java.io.BufferedInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;

public class Sound {
    public static boolean disableSound = false;

    // Use Clip for both WAV and MP3 now (via MP3SPI)
    private static final HashMap<String, Clip> clips = new HashMap<>();
    private static final HashMap<String, Boolean> loopingClips = new HashMap<>();

    public static void loadSound(String resourcePath) {
        // Now we can preload MP3s too if we want, or load on demand.
        // For consistency with previous logic, we check cache first.
        if (clips.containsKey(resourcePath))
            return;

        try {
            InputStream is = Sound.class.getResourceAsStream("/" + resourcePath);
            if (is == null) {
                System.out.println("Sound resource not found: " + resourcePath);
                return;
            }

            // BufferedInputStream is important for mark/reset support required by some
            // parsers
            InputStream bufferedIn = new BufferedInputStream(is);
            AudioInputStream audioStream = AudioSystem.getAudioInputStream(bufferedIn);

            // If it's an MP3 (or other encoded format), we might need to decode it to PCM
            AudioFormat baseFormat = audioStream.getFormat();
            AudioFormat decodedFormat = new AudioFormat(
                    AudioFormat.Encoding.PCM_SIGNED,
                    baseFormat.getSampleRate(),
                    16,
                    baseFormat.getChannels(),
                    baseFormat.getChannels() * 2,
                    baseFormat.getSampleRate(),
                    false);

            // Allow converting MP3 to PCM
            AudioInputStream decodedAudioStream = AudioSystem.getAudioInputStream(decodedFormat, audioStream);

            Clip clip = AudioSystem.getClip();
            clip.open(decodedAudioStream);
            clips.put(resourcePath, clip);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Error loading sound: " + resourcePath);
        }
    }

    public static void playSoundOnce(String resourcePath) {
        if (disableSound)
            return;

        Clip clip = getOrLoadClip(resourcePath);
        if (clip != null) {
            // Stop if currently playing, rewind, and play
            if (clip.isRunning()) {
                clip.stop();
            }
            clip.setFramePosition(0);
            clip.start();
        }
    }

    public static void playMusicOnLoop(String resourcePath) {
        if (disableSound)
            return;

        Clip clip = getOrLoadClip(resourcePath);
        if (clip != null) {
            if (clip.isRunning() && loopingClips.getOrDefault(resourcePath, false)) {
                return; // Already playing and looping
            }
            clip.setFramePosition(0);
            clip.loop(Clip.LOOP_CONTINUOUSLY);
            loopingClips.put(resourcePath, true);
            clip.start();
        }
    }

    public static void stopMusic(String resourcePath) {
        if (disableSound)
            return;

        Clip clip = clips.get(resourcePath);
        if (clip != null) {
            if (clip.isRunning()) {
                clip.stop();
            }
            loopingClips.remove(resourcePath);
        }
    }

    public static void stopAllSounds() {
        if (disableSound)
            return;

        for (String resourcePath : new ArrayList<>(clips.keySet())) {
            Clip clip = clips.get(resourcePath);
            if (clip != null && clip.isRunning()) {
                clip.stop();
            }
        }
        loopingClips.clear();
    }

    private static Clip getOrLoadClip(String resourcePath) {
        if (!clips.containsKey(resourcePath)) {
            loadSound(resourcePath);
        }
        return clips.get(resourcePath);
    }

    // Specific sound examples - use relative paths from resources root
    public static void click() {
        if (disableSound)
            return;
        playSoundOnce("music/click.wav");
    }

    public static void exitBall(Pokemon pkm) {
        playSoundOnce("music/catchFail.mp3");
        if (pkm.isShiny())
            playSoundOnce("music/shinySparkles.mp3");
    }
}
