package pokemonTextBased;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class TypingPromptRepository {
    private static final String WORD_RESOURCE = "typing/words.txt";
    private static final String SENTENCE_RESOURCE = "typing/sentences.txt";

    private static final List<String> WORDS = loadResourceLines(WORD_RESOURCE);
    private static final List<String> SENTENCES = loadResourceLines(SENTENCE_RESOURCE);

    private TypingPromptRepository() {
    }

    public static List<String> getWords() {
        return WORDS;
    }

    public static List<String> getSentences() {
        return SENTENCES;
    }

    private static List<String> loadResourceLines(String resourcePath) {
        InputStream inputStream = TypingPromptRepository.class.getClassLoader().getResourceAsStream(resourcePath);
        if (inputStream == null) {
            return Collections.emptyList();
        }

        List<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String normalized = line.trim().toLowerCase();
                if (!normalized.isBlank() && !normalized.startsWith("#")) {
                    lines.add(normalized);
                }
            }
        } catch (IOException e) {
            return Collections.emptyList();
        }
        return Collections.unmodifiableList(lines);
    }
}
