package beans;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Id;
import org.nutz.dao.entity.annotation.Table;
@Table("t_httpproxy")
public class HTTPProxy {
	@Column
	@Id
	private long proxyId;
	@Column
	private String address;
	@Column
	private int usedTimes;
	@Column
	private boolean checked;
	public long getProxyId() {
		return proxyId;
	}
	public void setProxyId(long proxyId) {
		this.proxyId = proxyId;
	}
	public String getAddress() {
		return address;
	}
	public void setAddress(String address) {
		this.address = address;
	}
	public int getUsedTimes() {
		return usedTimes;
	}
	public void setUsedTimes(int usedTimes) {
		this.usedTimes = usedTimes;
	}
	public boolean isChecked() {
		return checked;
	}
	public void setChecked(boolean checked) {
		this.checked = checked;
	}
}
