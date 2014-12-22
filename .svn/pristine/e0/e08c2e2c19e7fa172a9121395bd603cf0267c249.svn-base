package utils;

import java.net.MalformedURLException;

import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

import service.WeizhangService;

public class ProxyCheckTask implements Job {

	@Override
	public void execute(JobExecutionContext context)
			throws JobExecutionException {
		WeizhangService ws = (WeizhangService) context.getJobDetail()
				.getJobDataMap().get("WeizhangService");
		try {
			ws.proxyCheck();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
	}

}
