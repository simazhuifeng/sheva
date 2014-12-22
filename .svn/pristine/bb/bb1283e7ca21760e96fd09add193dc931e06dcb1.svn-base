package utils;

import java.awt.Frame;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.HashMap;

import javax.imageio.ImageIO;

import net.sourceforge.javaocr.ocrPlugins.mseOCR.CharacterRange;
import net.sourceforge.javaocr.ocrPlugins.mseOCR.OCRScanner;
import net.sourceforge.javaocr.ocrPlugins.mseOCR.TrainingImage;
import net.sourceforge.javaocr.ocrPlugins.mseOCR.TrainingImageLoader;

public class OCR {
	public static String getVerificationCode(BufferedImage src) throws MalformedURLException, IOException{
		BufferedImage bi = ImageOperations.Threshold(src, 150);
		BufferedImage dest = bi.getSubimage(3, 3, bi.getWidth() -6, bi.getHeight() - 6);
		ImageIO.write(dest, "jpg", new File("C:/Users/sheva.wen/Downloads/x.jpg"));
		OCRScanner ocrScanner = new OCRScanner();
		TrainingImageLoader loader = new TrainingImageLoader();
		HashMap<Character, ArrayList<TrainingImage>> trainingImages = new HashMap<Character, ArrayList<TrainingImage>>();
		Frame frame = new Frame();
		loader.load(
                frame,
                "conf/training.png",
                new CharacterRange('0','9'),
                trainingImages);
        ocrScanner.addTrainingImages(trainingImages);
        String text = ocrScanner.scan(dest, 0, 0, 0, 0, null);
        return text;
	}
}
