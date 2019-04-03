// test-service.cpp

//
#include "pch.h"

#include "common/wtools.h"
#include "tools/_misc.h"
#include "tools/_process.h"

#include "service_processor.h"

#include "service_api.h"

#include "windows_service_api.h"

namespace wtools {  // to become friendly for wtools classes
class TestProcessor : public wtools::BaseServiceProcessor {
public:
    TestProcessor() { s_counter++; }
    virtual ~TestProcessor() { s_counter--; }

    // Standard Windows API to Service hit here
    void stopService() { stopped_ = true; }
    void startService() { started_ = true; }
    void pauseService() { paused_ = true; }
    void continueService() { continued_ = true; }
    void shutdownService() { shutdowned_ = true; }
    const wchar_t* getMainLogName() const { return L"log.log"; }
    void preContextCall() { pre_context_call_ = true; }

    bool stopped_ = false;
    bool started_ = false;
    bool paused_ = false;
    bool shutdowned_ = false;
    bool continued_ = false;
    bool pre_context_call_ = false;
    static int s_counter;
};  // namespace wtoolsclassTestProcessor:publiccma::srv::BaseServiceProcessor
int TestProcessor::s_counter = 0;

#include <iostream>

TEST(ServiceControllerTest, CreateDelete) {
    using namespace std::chrono;
    {
        auto processor = new TestProcessor;
        wtools::ServiceController controller(processor);
        EXPECT_EQ(TestProcessor::s_counter, 1);
        EXPECT_FALSE(processor->started_ || processor->continued_ ||
                     processor->paused_ || processor->shutdowned_ ||
                     processor->stopped_);
        EXPECT_NE(controller.processor_, nullptr);
        EXPECT_EQ(controller.name_, nullptr);
        EXPECT_EQ(controller.can_stop_, false);
        EXPECT_EQ(controller.can_shutdown_, false);
        EXPECT_EQ(controller.can_pause_continue_, false);
        EXPECT_NE(controller.processor_, nullptr);
    }
    EXPECT_EQ(TestProcessor::s_counter, 0);
    EXPECT_EQ(ServiceController::s_controller_, nullptr);
}

TEST(ServiceControllerTest, InstallUninstall) {
    if (cma::tools::win::IsElevated()) {
        auto ret =
            wtools::InstallService(L"SN",         // name of service
                                   L"Test Name",  // service name to display
                                   SERVICE_DEMAND_START,  // start type
                                   nullptr,               // dependencies
                                   nullptr,               // no account
                                   nullptr                // no password
            );
        EXPECT_TRUE(ret);
        if (ret) wtools::UninstallService(L"SN");
    } else {
        XLOG::l(XLOG::kStdio).w("Skip Test - you have to be elevated");
    }
}

TEST(ServiceControllerTest, StartStop) {
    using namespace cma::srv;
    using namespace std::chrono;
    int counter = 0;
    auto processor =
        new ServiceProcessor(100ms, [&counter](const void* Processor) {
            xlog::l("pip").print();
            counter++;
            return true;
        });
    wtools::ServiceController controller(processor);
    EXPECT_NE(controller.processor_, nullptr);
    EXPECT_EQ(controller.name_, nullptr);
    EXPECT_EQ(controller.can_stop_, false);
    EXPECT_EQ(controller.can_shutdown_, false);
    EXPECT_EQ(controller.can_pause_continue_, false);
    EXPECT_NE(controller.processor_, nullptr);
    if (0) {
        auto ret =
            wtools::InstallService(L"SN",         // name of service
                                   L"Test Name",  // service name to display
                                   SERVICE_DEMAND_START,  // start type
                                   nullptr,               // dependencies
                                   nullptr,               // no account
                                   nullptr                // no password
            );
        EXPECT_TRUE(ret);
        if (ret) {
            bool success = false;
            std::thread t([&]() {
                success = controller.registerAndRun(L"SN", true, true, true);
            });
            EXPECT_TRUE(success);
            std::this_thread::sleep_until(steady_clock::now() +
                                          500ms);  // wait for thread
            EXPECT_TRUE(counter > 3);

            EXPECT_TRUE(ret);
            if (ret) wtools::UninstallService(L"SN");
        }
    }
}

}  // namespace wtools

TEST(ServiceApiTest, Base) {
    using namespace cma::install;
    using namespace cma::tools;
    auto msi = cma::cfg::GetMsiExecPath();
    EXPECT_TRUE(!msi.empty());
    auto path = win::GetSomeSystemFolder(FOLDERID_Public);
    std::ofstream f;
    try {
        // artificial file creation
        f.open(path + L"\\test.dat", std::ios::binary);
        char buf[] = "-----\n";
        f.write(buf, strlen(buf) + 1);
        f.close();

        // check for presence
        auto ret = IsFileExist(path + L"\\test.dat");
        EXPECT_TRUE(ret);

        // check MakTemp...
        auto to_install = MakeTempFileNameInTempPath(L"test.dat");
        EXPECT_TRUE(!to_install.empty());
        if (ret) {
            auto result =
                CheckForUpdateFile(L"test.dat", path, kMsiExecQuiet, false);
            EXPECT_TRUE(result);

            EXPECT_TRUE(IsFileExist(to_install));
            EXPECT_TRUE(!IsFileExist(path + L"\\test.dat"));
        }
    } catch (const std::exception& e) {
        xlog::l(XLOG_FLINE + "exception opening file %s", e.what());
    }
}

TEST(Misc, All) {
    {
        std::string a = "a";
        cma::tools::AddDirSymbol(a);
        EXPECT_TRUE(a == "a\\");
        cma::tools::AddDirSymbol(a);
        EXPECT_TRUE(a == "a\\");
    }
    {
        std::string b = "b\\";
        cma::tools::AddDirSymbol(b);
        EXPECT_TRUE(b == "b\\");
        b = "b/";
        cma::tools::AddDirSymbol(b);
        EXPECT_TRUE(b == "b/");
    }
}