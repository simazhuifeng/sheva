package beans.weizhang;

import java.util.Date;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Id;
import org.nutz.dao.entity.annotation.Table;

@Table("t_verificationcode")
public class VerificationCode {
	@Column
	@Id
	private long codeId;
	
	@Column
	private String code;
	
	@Column
	private String cookie;
	
	@Column
	private Date achieveTime;
	
	
	@Column
	private boolean used;


	public long getCodeId() {
		return codeId;
	}


	public void setCodeId(long codeId) {
		this.codeId = codeId;
	}


	public String getCode() {
		return code;
	}


	public void setCode(String code) {
		this.code = code;
	}


	public String getCookie() {
		return cookie;
	}


	public void setCookie(String cookie) {
		this.cookie = cookie;
	}


	public Date getAchieveTime() {
		return achieveTime;
	}


	public void setAchieveTime(Date achieveTime) {
		this.achieveTime = achieveTime;
	}


	public boolean isUsed() {
		return used;
	}


	public void setUsed(boolean used) {
		this.used = used;
	}
	
}
