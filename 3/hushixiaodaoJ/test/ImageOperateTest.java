import static org.junit.Assert.*;

import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import org.junit.Test;

import service.WeizhangService;
import utils.OCR;


public class ImageOperateTest {
	@Test
	public void getVerificationCode() throws IOException{
		//String code = OCR.getVerificationCode(ImageIO.read(new File("C:/Users/sheva.wen/Downloads/VerifyCodeServlet (2).jpg")));
		//assertTrue(code.equals("6618"));
		WeizhangService ws = new WeizhangService();
		String[] aa = ws.getVerificationCode_cookie("http://jjzd.nmgat.gov.cn/VerifyCodeServlet?timestamp=1385051268830");
		System.out.println(aa[0]);
		System.out.println(aa[1]);
	}
}
