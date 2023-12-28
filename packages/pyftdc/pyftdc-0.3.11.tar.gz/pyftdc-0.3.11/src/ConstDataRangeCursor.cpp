//
// Created by jorge on 1/7/21.
//
#include "include/ConstDataRangeCursor.h"
#include "spdlog/spdlog.h"


ConstDataRangeCursor::ConstDataRangeCursor(const uint8_t *data, size_t len) {
    this->data = data;
    this->length = len;

    this->start = this->data;
    this->at = this->data;
    this->end = this->start + this->length;
}

uint8_t
ConstDataRangeCursor::ReadByte() {

    if (at>=end) {
        spdlog::error("Out of bounds reading decompressed buffer.");
        throw std::runtime_error("out of bounds");
    }

    uint8_t val = *at;
    ++at;
    return val;
}
