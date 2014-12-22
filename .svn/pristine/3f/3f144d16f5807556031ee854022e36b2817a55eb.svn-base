var config = {
	dataSource : {
        type : "com.alibaba.druid.pool.DruidDataSource",
        events : {
            depose : 'close'
        },
        fields : {
        	driverClassName : {java :"$config.get('db-driver')"},
			url             : {java :"$config.get('db-url')"},
			username        : {java :"$config.get('db-username')"},
			password        : {java :"$config.get('db-password')"},
			testOnBorrow    : false
        }
	},
    dao : {
        type : "org.nutz.dao.impl.NutDao",
        fields : {
        	dataSource : {refer : 'dataSource'}
        }
    },
	config : {
		type : "org.nutz.ioc.impl.PropertiesProxy",
		fields : {
			paths : ["config.properties"]
		}
	},
    json : {
        type : "org.nutz.mvc.view.UTF8JsonView",
        args : [{
    		type : 'org.nutz.json.JsonFormat',
    		fields: {
    			autoUnicode : true
    		}
    	}]
    }
};