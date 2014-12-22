package service;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.MalformedURLException;
import java.net.Proxy;
import java.net.URL;
import java.net.URLConnection;
import java.net.UnknownHostException;
import java.util.List;

import javax.imageio.ImageIO;

import org.nutz.dao.Cnd;
import org.nutz.dao.Dao;
import org.nutz.mvc.Mvcs;

import utils.OCR;
import beans.HTTPProxy;

public class WeizhangService {
	Dao dao = Mvcs.getIoc().get(Dao.class);
	public String[] getVerificationCode_cookie(String url) throws IOException,UnknownHostException{
		URL obj = new URL(url);
		URLConnection conn = obj.openConnection();
		//get header by 'key'
		String cookie = conn.getHeaderField("Set-Cookie");
		BufferedImage src = ImageIO.read(conn.getInputStream());
		String code = OCR.getVerificationCode(src);
		return new String[]{code,cookie};
	}
	public HTTPProxy getProxy(){
		List<HTTPProxy> proxies =  dao.query(HTTPProxy.class, Cnd.where("usedtimes", "<", 5));
		if(proxies.iterator().hasNext()){
			return proxies.iterator().next();
		}else{
			return null;
		}
	}
	public void proxyCheck() throws MalformedURLException{
		List<HTTPProxy> proxies =  dao.query(HTTPProxy.class, Cnd.where("checked", "=", 0),dao.createPager(1, 10));
		for(HTTPProxy proxy : proxies){
			URL obj = new URL("http://jjzd.nmgat.gov.cn/Query.jsp");
				InetSocketAddress socketAddress;
				try {
					socketAddress = new InetSocketAddress(  
					        InetAddress.getByName(proxy.getAddress().split(":")[0]),
					        Integer.parseInt(proxy.getAddress().split(":")[1]));
			          
			        Proxy _proxy = new Proxy(Proxy.Type.HTTP,socketAddress); 
			        HttpURLConnection conn = (HttpURLConnection)obj.openConnection(_proxy);
			        conn.setConnectTimeout(2 * 1000);
			        conn.connect();
			        conn.getInputStream();
				} catch (Exception  e) {
					dao.delete(proxy);
				}  
		}
	}
}
