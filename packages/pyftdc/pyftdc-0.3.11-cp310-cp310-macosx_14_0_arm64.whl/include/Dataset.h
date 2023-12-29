//
// Created by jorge on 12/16/20.
//

#ifndef FTDCPARSER_DATASET_H
#define FTDCPARSER_DATASET_H

#include <string>
#include <vector>
#include <map>
#include <mutex>
#include <spdlog/logger.h>
#include <spdlog/spdlog.h>

#include "SampleLocation.h"
#include "FileParsedData.h"
#include "Timestamp.h"
#include "Metrics.h"
#include "MetricsToWTMap.h"

using namespace ftdcparser;

class Dataset {

public:
    static const int INVALID_TIMESTAMP_POS = INT_MAX;

    Dataset() :  samplesInDataset(0), start(INVALID_TIMESTAMP), end(INVALID_TIMESTAMP), metricNames(0){};
    explicit Dataset(const std::string& csvFileName);
    explicit Dataset(ParserState *pState, FileParsedData* fileParsedData);

    std::vector< std::string> const *getMetricsNames();
    MetricsPtr getMetric(std::string   metricName,
                         Timestamp start = INVALID_TIMESTAMP,
                         Timestamp end = INVALID_TIMESTAMP,
                         bool ratedMetric=false);

    FileParsedData*  getParsedFileInfo() {  return this->fileParsed; }
    std::vector<MetricsPtr> getMetrics( std::vector<std::string> metricNamesIn,
                                                 size_t start,  size_t end,
                                                 bool ratedMetrics);
    MetricsPtr getMetricMatrix(const std::vector<std::string>& metricNamesToReturn, size_t *stride,
                               Timestamp startLimit, Timestamp endLimit,
                               bool ratedMetrics);
    [[nodiscard]] Timestamp getStartTimestamp() const;
    [[nodiscard]] Timestamp getEndTimestamp() const;
    static std::string getJsonFromTimestamp(Timestamp ts);
    static std::string getCsvFromTimestamp(Timestamp ts);
    std::string getMetadata() { return parserState->getJSONMetadata();  }

    void buildFromFTDC();
    void buildFromFTDCThreaded();

    void buildFromParserState(const ParserState   *state);

private:
    FileParsedData *fileParsed{};
    bool ConvertToRatedMetric(MetricsPtr pVector);
    // Each chunk has its own list of metrics. This should be a list of metrics in the dataset,
    // with no guarantee that they appear in all BinaryBSONs.
    std::vector<std::string> metricNames;

    ParserState *parserState{0};
    size_t samplesInDataset{0};

    Timestamp start;
    Timestamp end;
};

#endif //FTDCPARSER_DATASET_H
